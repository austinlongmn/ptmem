import pytest
import tempfile
import os
from unittest.mock import patch
from ptmem.main import main


class TestPTMemCLI:
    """Test suite for PTMem command-line interface"""

    def test_help_message(self):
        """Test that help message is displayed correctly"""
        with patch("sys.argv", ["ptmem", "--help"]):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 0

    def test_missing_arguments(self):
        """Test error handling when required arguments are missing"""
        with patch("sys.argv", ["ptmem"]):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 2  # argparse error code

    def test_missing_output_argument(self):
        """Test error handling when output argument is missing"""
        with patch("sys.argv", ["ptmem", "input.ptmem"]):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 2  # argparse error code

    def test_invalid_output_type(self):
        """Test error handling for invalid output type"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write("# Test\n\n- Question?\n+ Answer\n")
            input_file.flush()

            try:
                with patch(
                    "sys.argv",
                    ["ptmem", input_file.name, "output.json", "-t", "invalid"],
                ):
                    with pytest.raises(SystemExit) as excinfo:
                        main()
                    assert excinfo.value.code == 2  # argparse error code
            finally:
                os.unlink(input_file.name)

    def test_json_output_type_explicit(self):
        """Test explicit JSON output type specification"""
        ptmem_content = """# Test

- Test question?
+ Test answer
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write(ptmem_content)
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as output_file:
                try:
                    with patch(
                        "sys.argv",
                        ["ptmem", input_file.name, output_file.name, "-t", "json"],
                    ):
                        main()

                    # Verify file was created and contains JSON
                    assert os.path.exists(output_file.name)
                    with open(output_file.name, "r") as f:
                        import json

                        result = json.load(f)
                        assert len(result) == 1
                        assert result[0]["questions"] == ["Test question?"]
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_flash_output_type_explicit(self):
        """Test explicit fla.sh output type specification"""
        ptmem_content = """# Test

- Test question?
+ Test answer
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write(ptmem_content)
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".flash", delete=False
            ) as output_file:
                try:
                    with patch(
                        "sys.argv",
                        [
                            "ptmem",
                            input_file.name,
                            output_file.name,
                            "--output-type",
                            "fla.sh",
                        ],
                    ):
                        main()

                    # Verify file was created and contains flash format
                    assert os.path.exists(output_file.name)
                    with open(output_file.name, "r") as f:
                        lines = [line.strip() for line in f.readlines()]
                        assert len(lines) == 1
                        assert lines[0] == "Test:Test question?:Test answer:0"
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_nonexistent_input_file(self):
        """Test error handling for non-existent input file"""
        with patch("sys.argv", ["ptmem", "nonexistent.ptmem", "output.json"]):
            with pytest.raises(FileNotFoundError):
                main()

    def test_permission_denied_output_file(self):
        """Test error handling when output file cannot be written"""
        ptmem_content = """# Test

- Test question?
+ Test answer
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write(ptmem_content)
            input_file.flush()

            # Try to write to a directory that doesn't exist
            invalid_output_path = "/nonexistent/directory/output.json"

            try:
                with patch("sys.argv", ["ptmem", input_file.name, invalid_output_path]):
                    with pytest.raises((FileNotFoundError, PermissionError, OSError)):
                        main()
            finally:
                os.unlink(input_file.name)

    def test_empty_input_file_handling(self):
        """Test handling of empty input files"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write("")  # Empty file
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as output_file:
                try:
                    with patch(
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    # Should create empty JSON array
                    with open(output_file.name, "r") as f:
                        import json

                        result = json.load(f)
                        assert result == []
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_stdin_dash_argument(self):
        """Test using '-' as input file to read from stdin"""
        ptmem_content = """# Stdin Test

- From stdin?
+ Yes, from stdin
"""
        from io import StringIO

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as output_file:
            try:
                with patch("sys.stdin", StringIO(ptmem_content)):
                    with patch("sys.argv", ["ptmem", "-", output_file.name]):
                        main()

                with open(output_file.name, "r") as f:
                    import json

                    result = json.load(f)
                    assert len(result) == 1
                    assert result[0]["questions"] == ["From stdin?"]
                    assert result[0]["answers"] == ["Yes, from stdin"]
                    assert result[0]["category"] == "Stdin Test"
            finally:
                os.unlink(output_file.name)

    def test_argument_order_flexibility(self):
        """Test that arguments work in different orders"""
        ptmem_content = """# Order Test

- Does order matter?
+ No, it shouldn't
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write(ptmem_content)
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as output_file:
                try:
                    # Test with output type flag before files
                    with patch(
                        "sys.argv",
                        [
                            "ptmem",
                            "--output-type",
                            "json",
                            input_file.name,
                            output_file.name,
                        ],
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        import json

                        result = json.load(f)
                        assert len(result) == 1
                        assert result[0]["questions"] == ["Does order matter?"]
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_short_and_long_flags(self):
        """Test both short (-t) and long (--output-type) flag versions"""
        ptmem_content = """# Flag Test

- Short or long?
+ Both work
"""

        # Test short flag
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write(ptmem_content)
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".flash", delete=False
            ) as output_file:
                try:
                    with patch(
                        "sys.argv",
                        ["ptmem", input_file.name, output_file.name, "-t", "fla.sh"],
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        lines = [line.strip() for line in f.readlines()]
                        assert len(lines) == 1
                        assert "Flag Test:Short or long?:Both work:0" == lines[0]
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

        # Test long flag
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write(ptmem_content)
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".flash", delete=False
            ) as output_file:
                try:
                    with patch(
                        "sys.argv",
                        [
                            "ptmem",
                            input_file.name,
                            output_file.name,
                            "--output-type",
                            "fla.sh",
                        ],
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        lines = [line.strip() for line in f.readlines()]
                        assert len(lines) == 1
                        assert "Flag Test:Short or long?:Both work:0" == lines[0]
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_default_output_type(self):
        """Test that JSON is the default output type when not specified"""
        ptmem_content = """# Default Test

- What's the default?
+ JSON format
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write(ptmem_content)
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as output_file:
                try:
                    # No output type specified, should default to JSON
                    with patch(
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        import json

                        result = json.load(f)
                        assert len(result) == 1
                        assert result[0]["questions"] == ["What's the default?"]
                        assert result[0]["answers"] == ["JSON format"]
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)
