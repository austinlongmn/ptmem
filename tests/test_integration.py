import json
import tempfile
import os
from unittest.mock import patch
from ptmem.main import main


class TestPTMemIntegration:
    """Integration tests using fixture files"""

    def test_sample_file_to_json(self):
        """Test converting the sample PTMem file to JSON"""
        sample_file = "tests/fixtures/sample.ptmem"
        expected_file = "tests/fixtures/sample_expected.json"

        # Load expected results
        with open(expected_file, "r") as f:
            expected = json.load(f)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as output_file:
            try:
                with patch("sys.argv", ["ptmem", sample_file, output_file.name]):
                    main()

                with open(output_file.name, "r") as f:
                    result = json.load(f)

                assert result == expected
            finally:
                os.unlink(output_file.name)

    def test_sample_file_to_flash(self):
        """Test converting the sample PTMem file to fla.sh format"""
        sample_file = "tests/fixtures/sample.ptmem"

        expected_lines = [
            "Mathematics:What is 2 + 2?:4:0",
            "Mathematics:What is the square root of 16?:4:0",
            "Mathematics:What are the first three prime numbers?:2; 3; 5:0",
            "Science:What is the chemical symbol for water?:H2O:0",
            "Science:What gas do plants absorb during photosynthesis?:Carbon dioxide; CO2:0",
            "Science:Who developed the theory of relativity?:Albert Einstein:0",
            "History:When did World War II end?:1945:0",
            "History:Who was the first president of the United States?:George Washington:0",
            "History:In what year did the Berlin Wall fall?:1989:0",
            "Geography:What is the capital of France?; What city is the capital of France?:Paris:0",
            "Geography:Which is the largest ocean?:Pacific Ocean:0",
            "Geography:What are the seven continents?:Asia; Africa; North America; South America; Antarctica; Europe; Australia:0",
            'Literature:Who wrote "Romeo and Juliet"?:William Shakespeare:0',
            "Literature:What is the first book in the Harry Potter series?:Harry Potter and the Philosopher's Stone; Harry Potter and the Sorcerer's Stone:0",
            "Programming:What does CPU stand for?:Central Processing Unit:0",
            'Programming:What programming language is known for "write once, run anywhere"?:Java:0',
            "Programming:What does HTML stand for?:HyperText Markup Language:0",
        ]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".flash", delete=False
        ) as output_file:
            try:
                with patch(
                    "sys.argv", ["ptmem", sample_file, output_file.name, "-t", "fla.sh"]
                ):
                    main()

                with open(output_file.name, "r") as f:
                    result_lines = [line.strip() for line in f.readlines()]

                assert result_lines == expected_lines
            finally:
                os.unlink(output_file.name)

    def test_roundtrip_consistency(self):
        """Test that converting to JSON and back produces consistent results"""
        sample_file = "tests/fixtures/sample.ptmem"

        # First conversion to JSON
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as json_output:
            try:
                with patch("sys.argv", ["ptmem", sample_file, json_output.name]):
                    main()

                # Load the JSON result
                with open(json_output.name, "r") as f:
                    first_result = json.load(f)

                # Second conversion to JSON (should be identical)
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".json", delete=False
                ) as json_output2:
                    try:
                        with patch(
                            "sys.argv", ["ptmem", sample_file, json_output2.name]
                        ):
                            main()

                        with open(json_output2.name, "r") as f:
                            second_result = json.load(f)

                        assert first_result == second_result
                    finally:
                        os.unlink(json_output2.name)
            finally:
                os.unlink(json_output.name)

    def test_empty_fixture_handling(self):
        """Test handling of an empty fixture file"""
        empty_content = ""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as empty_file:
            empty_file.write(empty_content)
            empty_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as output_file:
                try:
                    with patch(
                        "sys.argv", ["ptmem", empty_file.name, output_file.name]
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    assert result == []
                finally:
                    os.unlink(empty_file.name)
                    os.unlink(output_file.name)

    def test_large_file_performance(self):
        """Test performance with a larger generated file"""
        # Generate a larger PTMem file
        large_content = []
        for category_num in range(10):
            category_name = f"Category {category_num + 1}"
            large_content.append(f"# {category_name}")
            large_content.append("")

            for card_num in range(20):
                large_content.append(f"- Question {card_num + 1} in {category_name}?")
                for answer_num in range(3):
                    large_content.append(f"+ Answer {answer_num + 1}")
                large_content.append("")

        large_ptmem_content = "\n".join(large_content)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as large_file:
            large_file.write(large_ptmem_content)
            large_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as output_file:
                try:
                    import time

                    start_time = time.time()

                    with patch(
                        "sys.argv", ["ptmem", large_file.name, output_file.name]
                    ):
                        main()

                    end_time = time.time()
                    processing_time = end_time - start_time

                    # Should complete within reasonable time (adjust as needed)
                    assert processing_time < 5.0  # 5 seconds max

                    # Verify correct number of cards
                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    # 10 categories * 20 cards each = 200 cards
                    assert len(result) == 200

                    # Verify structure of first and last cards
                    assert result[0]["category"] == "Category 1"
                    assert len(result[0]["answers"]) == 3
                    assert result[-1]["category"] == "Category 10"

                finally:
                    os.unlink(large_file.name)
                    os.unlink(output_file.name)

    def test_mixed_format_compatibility(self):
        """Test that both JSON and fla.sh outputs contain the same information"""
        sample_file = "tests/fixtures/sample.ptmem"

        # Convert to JSON
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as json_output:
            with patch("sys.argv", ["ptmem", sample_file, json_output.name]):
                main()

            with open(json_output.name, "r") as f:
                json_result = json.load(f)

        # Convert to fla.sh
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".flash", delete=False
        ) as flash_output:
            with patch(
                "sys.argv", ["ptmem", sample_file, flash_output.name, "-t", "fla.sh"]
            ):
                main()

            with open(flash_output.name, "r") as f:
                flash_lines = [line.strip() for line in f.readlines()]

        try:
            # Verify same number of cards
            assert len(json_result) == len(flash_lines)

            # Verify content matches (compare first few cards)
            for i in range(min(3, len(json_result))):
                json_card = json_result[i]
                flash_parts = flash_lines[i].split(":")

                # Extract components from flash format
                flash_category = flash_parts[0]
                flash_questions = flash_parts[1].split("; ")
                flash_answers = flash_parts[2].split("; ")

                # Compare
                assert json_card["category"] == flash_category
                assert json_card["questions"] == flash_questions
                assert json_card["answers"] == flash_answers

        finally:
            os.unlink(json_output.name)
            os.unlink(flash_output.name)

    def test_file_encoding_handling(self):
        """Test handling of files with different encodings"""
        # Create file with UTF-8 characters
        utf8_content = """# Encoding Test

- What does 你好 mean?
+ Hello in Chinese

- What is π (pi)?
+ Approximately 3.14159
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False, encoding="utf-8"
        ) as utf8_file:
            utf8_file.write(utf8_content)
            utf8_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as output_file:
                try:
                    with patch("sys.argv", ["ptmem", utf8_file.name, output_file.name]):
                        main()

                    with open(output_file.name, "r", encoding="utf-8") as f:
                        result = json.load(f)

                    # Verify UTF-8 characters are preserved
                    assert len(result) == 2
                    assert "你好" in result[0]["questions"][0]
                    assert "π" in result[1]["questions"][0]

                finally:
                    os.unlink(utf8_file.name)
                    os.unlink(output_file.name)
