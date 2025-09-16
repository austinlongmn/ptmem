# PTMem Test Suite

This directory contains comprehensive tests for the PTMem flash card file format parser and converter.

## Overview

The test suite is organized into several modules, each testing different aspects of the PTMem application:

- **`test_main.py`** - Core functionality tests for the PTMem parser
- **`test_edge_cases.py`** - Edge cases and error handling tests
- **`test_cli.py`** - Command-line interface and argument parsing tests
- **`test_integration.py`** - End-to-end integration tests using fixture files
- **`fixtures/`** - Sample test files and expected outputs

## Test Categories

### Core Functionality Tests (`test_main.py`)
- Basic card parsing (single question, single answer)
- Multiple cards parsing
- Multiple questions per card
- Multiple answers per card
- Comment handling (lines starting with `/ `)
- Category parsing (lines starting with `# `)
- Blank line separation between cards
- stdin input handling
- JSON output format
- fla.sh output format with confidence score preservation
- Whitespace handling
- Special character support
- Unicode character support

### Edge Cases (`test_edge_cases.py`)
- Questions without answers (should be ignored)
- Answers without questions (should be ignored)
- Cards without categories (category = null)
- Multiple consecutive blank lines
- Lines with only prefixes (no content)
- Very long content handling
- Malformed existing fla.sh files
- Mixed line endings (\\n, \\r\\n, \\r)
- Empty categories
- Colons in content for fla.sh format

### CLI Tests (`test_cli.py`)
- Help message display
- Missing argument handling
- Invalid output type handling
- Explicit output type specification
- Non-existent input file handling
- Permission errors
- Empty file handling
- stdin input with `-` argument
- Argument order flexibility
- Short (`-t`) and long (`--output-type`) flag versions
- Default output type behavior

### Integration Tests (`test_integration.py`)
- Full sample file conversion to JSON
- Full sample file conversion to fla.sh format
- Roundtrip consistency testing
- Large file performance testing
- Format compatibility verification
- File encoding handling (UTF-8)

## File Formats Tested

### PTMem Input Format
```
# Category Name

- Question text
+ Answer text

- Another question
+ Answer 1
+ Answer 2

/ This is a comment (ignored)
```

### JSON Output Format
```json
[
    {
        "questions": ["Question text"],
        "answers": ["Answer text"],
        "category": "Category Name"
    }
]
```

### fla.sh Output Format
```
Category Name:Question text:Answer text:0
Category Name:Question with multiple answers:Answer 1; Answer 2:0
```

## Running Tests

### Using the Test Runner Script
```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --unit          # Core functionality only
python run_tests.py --edge          # Edge cases only
python run_tests.py --cli           # CLI tests only
python run_tests.py --integration   # Integration tests only

# Run with coverage report
python run_tests.py --coverage

# Install dependencies and run tests
python run_tests.py --install-deps

# Run tests matching a pattern
python run_tests.py "test_basic"
```

### Using pytest Directly
```bash
# Install test dependencies
pip install -e .[test]

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_main.py

# Run specific test method
pytest tests/test_main.py::TestPTMemParser::test_basic_card_parsing

# Run with coverage
pytest tests/ --cov=src/ptmem --cov-report=html
```

## Test Fixtures

The `fixtures/` directory contains:

- **`sample.ptmem`** - A comprehensive sample PTMem file with multiple categories, various question/answer combinations, comments, and Unicode characters
- **`sample_expected.json`** - The expected JSON output for the sample file

These fixtures are used in integration tests to ensure the parser handles real-world files correctly.

## Test Coverage

The test suite aims for comprehensive coverage of:

- ✅ All PTMem syntax elements (categories, questions, answers, comments)
- ✅ Both output formats (JSON and fla.sh)
- ✅ Command-line interface and arguments
- ✅ Error handling and edge cases
- ✅ File I/O operations
- ✅ Unicode and special character handling
- ✅ Performance with larger files
- ✅ Confidence score preservation in fla.sh format

## Adding New Tests

When adding new tests:

1. **Choose the appropriate test file** based on what you're testing
2. **Follow the existing naming convention** (`test_descriptive_name`)
3. **Use temporary files** for file I/O tests to avoid cluttering the filesystem
4. **Clean up resources** in `finally` blocks or use context managers
5. **Test both success and failure cases** where applicable
6. **Add docstrings** explaining what each test validates

### Example Test Structure
```python
def test_new_feature(self):
    """Test description of what this validates"""
    # Arrange
    input_content = "test content"
    expected_result = {"expected": "output"}
    
    # Act
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as input_file:
        input_file.write(input_content)
        input_file.flush()
        
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
            try:
                with patch("sys.argv", ["ptmem", input_file.name, output_file.name]):
                    main()
                
                # Assert
                with open(output_file.name, "r") as f:
                    result = json.load(f)
                
                assert result == expected_result
            finally:
                os.unlink(input_file.name)
                os.unlink(output_file.name)
```

## Dependencies

Test dependencies are defined in `pyproject.toml` under `[project.optional-dependencies]`:

- `pytest>=7.0.0` - Test framework
- `pytest-cov>=4.0.0` - Coverage reporting

Optional dependencies for enhanced testing:
- `pytest-xdist` - Parallel test execution
- `pytest-mock` - Enhanced mocking capabilities

## Continuous Integration

These tests are designed to run in CI/CD environments and provide:

- Clear pass/fail indicators
- Detailed error messages
- Coverage reporting
- Performance benchmarks
- Cross-platform compatibility testing

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'ptmem'**
   - Install the package in development mode: `pip install -e .`

2. **FileNotFoundError for fixture files**
   - Ensure you're running tests from the project root directory
   - Check that fixture files exist in `tests/fixtures/`

3. **Permission denied errors**
   - Tests create temporary files; ensure write permissions in temp directory

4. **Test failures on Windows**
   - Line ending differences may cause issues; tests handle mixed line endings

### Getting Help

If you encounter issues with the test suite:

1. Check that all dependencies are installed: `pip install -e .[test]`
2. Run tests with verbose output: `python run_tests.py -v`
3. Check individual test files for more specific error messages
4. Ensure the PTMem package is properly installed in development mode