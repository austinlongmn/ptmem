import json
import tempfile
import os
from io import StringIO
from unittest.mock import patch
from ptmem.main import main


class TestPTMemParser:
    """Test suite for PTMem file parser"""

    def test_basic_card_parsing(self):
        """Test parsing a basic PTMem file with one card"""
        ptmem_content = """# Math

- What is 2 + 2?
+ 4
"""
        expected = [
            {"questions": ["What is 2 + 2?"], "answers": ["4"], "category": "Math"}
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
                    # Test the main function
                    with patch(
                        "sys.argv", ["ptmem", input_file.name, output_file.name]
                    ):
                        main()

                    # Read and verify the output
                    with open(output_file.name, "r") as f:
                        result = json.load(f)

                    assert result == expected
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_multiple_cards(self):
        """Test parsing multiple cards"""
        ptmem_content = """# History

- When did World War II end?
+ 1945

- Who was the first US president?
+ George Washington
"""
        expected = [
            {
                "questions": ["When did World War II end?"],
                "answers": ["1945"],
                "category": "History",
            },
            {
                "questions": ["Who was the first US president?"],
                "answers": ["George Washington"],
                "category": "History",
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

    def test_multiple_answers(self):
        """Test parsing cards with multiple answers"""
        ptmem_content = """# Science

- What are the primary colors?
+ Red
+ Blue
+ Yellow
"""
        expected = [
            {
                "questions": ["What are the primary colors?"],
                "answers": ["Red", "Blue", "Yellow"],
                "category": "Science",
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

    def test_multiple_questions(self):
        """Test parsing cards with multiple questions"""
        ptmem_content = """# Geography

- What is the capital of France?
- What city is the capital of France?
+ Paris
"""
        expected = [
            {
                "questions": [
                    "What is the capital of France?",
                    "What city is the capital of France?",
                ],
                "answers": ["Paris"],
                "category": "Geography",
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

    def test_comments_ignored(self):
        """Test that comments are properly ignored"""
        ptmem_content = """# Literature

/ This is a comment
- Who wrote Romeo and Juliet?
/ Another comment
+ William Shakespeare
/ Final comment
"""
        expected = [
            {
                "questions": ["Who wrote Romeo and Juliet?"],
                "answers": ["William Shakespeare"],
                "category": "Literature",
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

    def test_multiple_categories(self):
        """Test parsing cards from multiple categories"""
        ptmem_content = """# Math

- What is 2 + 2?
+ 4

# Science

- What is H2O?
+ Water
"""
        expected = [
            {"questions": ["What is 2 + 2?"], "answers": ["4"], "category": "Math"},
            {
                "questions": ["What is H2O?"],
                "answers": ["Water"],
                "category": "Science",
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

    def test_empty_file(self):
        """Test parsing an empty file"""
        ptmem_content = ""
        expected = []

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

    def test_only_comments(self):
        """Test file with only comments"""
        ptmem_content = """/ This is just a comment
/ Another comment
/ One more comment
"""
        expected = []

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

    def test_card_without_blank_line_at_end(self):
        """Test that the last card is processed even without a trailing blank line"""
        ptmem_content = """# Programming

- What does CPU stand for?
+ Central Processing Unit"""
        expected = [
            {
                "questions": ["What does CPU stand for?"],
                "answers": ["Central Processing Unit"],
                "category": "Programming",
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

    def test_stdin_input(self):
        """Test reading from stdin"""
        ptmem_content = """# Test

- Test question?
+ Test answer
"""
        expected = [
            {
                "questions": ["Test question?"],
                "answers": ["Test answer"],
                "category": "Test",
            }
        ]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as output_file:
            try:
                with patch("sys.stdin", StringIO(ptmem_content)):
                    with patch("sys.argv", ["ptmem", "-", output_file.name]):
                        main()

                with open(output_file.name, "r") as f:
                    result = json.load(f)

                assert result == expected
            finally:
                os.unlink(output_file.name)

    def test_flash_output_format_new_file(self):
        """Test fla.sh output format for new file"""
        ptmem_content = """# Math

- What is 2 + 2?
+ 4

- What is 3 + 3?
+ 6
"""
        expected_lines = ["Math:What is 2 + 2?:4:0", "Math:What is 3 + 3?:6:0"]

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

    def test_flash_output_format_preserve_confidence(self):
        """Test fla.sh output format preserves existing confidence scores"""
        ptmem_content = """# Math

- What is 2 + 2?
+ 4

- What is 5 + 5?
+ 10
"""
        existing_flash_content = """Math:What is 2 + 2?:4:3
Math:What is 3 + 3?:6:2
"""
        expected_lines = [
            "Math:What is 2 + 2?:4:3",  # Preserved confidence
            "Math:What is 5 + 5?:10:0",  # New card with default confidence
        ]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False
        ) as input_file:
            input_file.write(ptmem_content)
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".flash", delete=False
            ) as output_file:
                # Pre-populate output file with existing content
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

                    assert result_lines == expected_lines
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)

    def test_flash_output_multiple_questions_answers(self):
        """Test fla.sh output format with multiple questions and answers"""
        ptmem_content = """# Science

- What are noble gases?
- Which gases are noble?
+ Helium
+ Neon
+ Argon
"""
        expected_lines = [
            "Science:What are noble gases?; Which gases are noble?:Helium; Neon; Argon:0"
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

    def test_whitespace_handling(self):
        """Test that leading/trailing whitespace is properly handled"""
        ptmem_content = """  # Whitespace Test

  - What is this?
  + This is a test

"""
        expected = [
            {
                "questions": ["What is this?"],
                "answers": ["This is a test"],
                "category": "Whitespace Test",
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

    def test_special_characters(self):
        """Test handling of special characters in content"""
        ptmem_content = """# Special Characters

- What symbols are these: @#$%^&*(){}[]?
+ Special symbols: @#$%^&*(){}[]

- What about quotes: "Hello" and 'World'?
+ They are quotation marks
"""
        expected = [
            {
                "questions": ["What symbols are these: @#$%^&*(){}[]?"],
                "answers": ["Special symbols: @#$%^&*(){}[]"],
                "category": "Special Characters",
            },
            {
                "questions": ["What about quotes: \"Hello\" and 'World'?"],
                "answers": ["They are quotation marks"],
                "category": "Special Characters",
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

    def test_unicode_characters(self):
        """Test handling of Unicode characters"""
        ptmem_content = """# Unicode

- What does 你好 mean?
+ Hello in Chinese

- Mathematical symbol: ∑
+ Summation
"""
        expected = [
            {
                "questions": ["What does 你好 mean?"],
                "answers": ["Hello in Chinese"],
                "category": "Unicode",
            },
            {
                "questions": ["Mathematical symbol: ∑"],
                "answers": ["Summation"],
                "category": "Unicode",
            },
        ]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ptmem", delete=False, encoding="utf-8"
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

                    with open(output_file.name, "r", encoding="utf-8") as f:
                        result = json.load(f)

                    assert result == expected
                finally:
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)
