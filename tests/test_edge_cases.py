import json
import tempfile
import os
from unittest.mock import patch
from ptmem.main import main


class TestPTMemEdgeCases:
    """Test suite for PTMem edge cases and error conditions"""

    def test_question_without_answer(self):
        """Test that questions without answers are included with empty answers"""
        ptmem_content = """# Incomplete

- Question with no answer

- Complete question
+ Complete answer
"""
        expected = [
            {
                "questions": ["Question with no answer"],
                "answers": [],
                "category": "Incomplete",
            },
            {
                "questions": ["Complete question"],
                "answers": ["Complete answer"],
                "category": "Incomplete",
            },
        ]

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
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    assert result == expected
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_answer_without_question(self):
        """Test that answers without questions get attached to next valid card"""
        ptmem_content = """# Orphaned Answers

+ Orphaned answer 1
+ Orphaned answer 2

- Valid question
+ Valid answer
"""
        expected = [
            {
                "questions": ["Valid question"],
                "answers": ["Orphaned answer 1", "Orphaned answer 2", "Valid answer"],
                "category": "Orphaned Answers",
            }
        ]

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
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    assert result == expected
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_card_without_category(self):
        """Test cards that appear before any category is defined"""
        ptmem_content = """- Question before category
+ Answer before category

# Proper Category

- Question with category
+ Answer with category
"""
        expected = [
            {
                "questions": ["Question before category"],
                "answers": ["Answer before category"],
                "category": None,
            },
            {
                "questions": ["Question with category"],
                "answers": ["Answer with category"],
                "category": "Proper Category",
            },
        ]

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
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    assert result == expected
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_multiple_blank_lines(self):
        """Test handling of multiple consecutive blank lines"""
        ptmem_content = """# Test Category



- First question
+ First answer



- Second question
+ Second answer



"""
        expected = [
            {
                "questions": ["First question"],
                "answers": ["First answer"],
                "category": "Test Category",
            },
            {
                "questions": ["Second question"],
                "answers": ["Second answer"],
                "category": "Test Category",
            },
        ]

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
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    assert result == expected
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_lines_with_only_prefixes(self):
        """Test lines that only contain the prefixes without content"""
        ptmem_content = """# Empty Lines Test

#
-
+
/
- Real question
+ Real answer
"""
        expected = [
            {
                "questions": ["Real question"],
                "answers": ["Real answer"],
                "category": "Empty Lines Test",
            }
        ]

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
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    assert result == expected
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_very_long_content(self):
        """Test handling of very long questions and answers"""
        long_question = "What is " + "very " * 100 + "long question?"
        long_answer = "This is a " + "very " * 100 + "long answer."

        ptmem_content = f"""# Long Content

- {long_question}
+ {long_answer}
"""
        expected = [
            {
                "questions": [long_question],
                "answers": [long_answer],
                "category": "Long Content",
            }
        ]

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
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    assert result == expected
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_malformed_flash_file_preservation(self):
        """Test handling of malformed existing flash files during preservation"""
        ptmem_content = """# Math

- What is 2 + 2?
+ 4
"""
        # Malformed existing content with various line formats
        existing_flash_content = """Math:What is 2 + 2?:4:3
malformed_line_without_colons
line:with:only:two:colons
:empty:start:field:2
Math:Another:Question:Answer:5:extra:fields
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write(ptmem_content)
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".flash", delete=False
            ) as output_file:
                # Pre-populate output file with malformed content
                with open(output_file.name, "w") as f:
                    f.write(existing_flash_content)

                try:
                    with patch(
                        "sys.argv",
                        ["ptmem", input_file.name, output_file.name, "-t", "fla.sh"],
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        result_lines = [line.strip() for line in f.readlines()]

                    # Should preserve the valid matching line and add new content
                    expected_lines = ["Math:What is 2 + 2?:4:3"]
                    assert result_lines == expected_lines
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_mixed_line_endings(self):
        """Test handling of mixed line endings (\\n, \\r\\n, \\r)"""
        # Create content with mixed line endings
        ptmem_content = "# Mixed Endings\r\n\r\n- Question 1?\r+ Answer 1\n\n- Question 2?\r\n+ Answer 2\r"
        expected = [
            {
                "questions": ["Question 1?"],
                "answers": ["Answer 1"],
                "category": "Mixed Endings",
            },
            {
                "questions": ["Question 2?"],
                "answers": ["Answer 2"],
                "category": "Mixed Endings",
            },
        ]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False, newline=""
        ) as input_file:
            input_file.write(ptmem_content)
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as output_file:
                try:
                    with patch(
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    assert result == expected
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_invalid_category_line(self):
        """Test that lines starting with # but without space are not treated as categories"""
        ptmem_content = """#InvalidCategory

- Question under no category
+ Answer

# Valid Category

- Question under valid category
+ Answer 2
"""
        expected = [
            {
                "questions": ["Question under no category"],
                "answers": ["Answer"],
                "category": None,  # No valid category was set before this card
            },
            {
                "questions": ["Question under valid category"],
                "answers": ["Answer 2"],
                "category": "Valid Category",
            },
        ]

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
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    assert result == expected
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_flash_format_with_colons_in_content(self):
        """Test fla.sh format with colons in questions/answers"""
        ptmem_content = """# Time

- What time is it at 12:30 PM?
+ It's 12:30 PM: afternoon time
"""
        # The colons in content should be preserved in the flash format
        expected_lines = [
            "Time:What time is it at 12:30 PM?:It's 12:30 PM: afternoon time:0"
        ]

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
                        result_lines = [line.strip() for line in f.readlines()]

                    assert result_lines == expected_lines
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)
