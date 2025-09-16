#!/usr/bin/env python3
"""
Test runner script for PTMem
Provides an easy way to run all tests with various options.
"""

import sys
import subprocess
import argparse
import os
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return the result."""
    if description:
        print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)

    result = subprocess.run(cmd, capture_output=False)
    print("-" * 50)

    if result.returncode == 0:
        print(f"✅ SUCCESS: {description or 'Command completed'}")
    else:
        print(f"❌ FAILED: {description or 'Command failed'}")

    print()
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run PTMem tests")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Run tests with verbose output"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Run tests with coverage report"
    )
    parser.add_argument(
        "--unit", action="store_true", help="Run only unit tests (test_main.py)"
    )
    parser.add_argument(
        "--edge",
        action="store_true",
        help="Run only edge case tests (test_edge_cases.py)",
    )
    parser.add_argument(
        "--cli", action="store_true", help="Run only CLI tests (test_cli.py)"
    )
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run only integration tests (test_integration.py)",
    )
    parser.add_argument(
        "--fast", action="store_true", help="Run tests with minimal output"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel (requires pytest-xdist)",
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install test dependencies before running",
    )
    parser.add_argument(
        "pattern", nargs="?", help="Pattern to match specific test files or functions"
    )

    args = parser.parse_args()

    # Change to the project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)

    # Install dependencies if requested
    if args.install_deps:
        print("Installing test dependencies...")
        install_cmd = ["uv", "add", "--dev", "pytest", "pytest-cov"]
        if run_command(install_cmd, "Installing test dependencies") != 0:
            print("Failed to install dependencies. Continuing anyway...")
        print()

    # Build the pytest command
    cmd = ["uv", "run", "pytest"]

    # Add test discovery path
    cmd.append("tests/")

    # Handle specific test selections
    if args.unit:
        cmd.append("tests/test_main.py")
    elif args.edge:
        cmd.append("tests/test_edge_cases.py")
    elif args.cli:
        cmd.append("tests/test_cli.py")
    elif args.integration:
        cmd.append("tests/test_integration.py")
    elif args.pattern:
        cmd.extend(["-k", args.pattern])

    # Add verbosity options
    if args.verbose:
        cmd.extend(["-v", "-s"])
    elif args.fast:
        cmd.extend(["-q", "--tb=no"])
    else:
        cmd.append("-v")

    # Add coverage if requested
    if args.coverage:
        cmd.extend(
            [
                "--cov=src/ptmem",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov",
            ]
        )

    # Add parallel execution if requested
    if args.parallel:
        cmd.extend(["-n", "auto"])

    # Run the tests
    print("🧪 Starting PTMem Test Suite")
    print("=" * 60)

    exit_code = run_command(cmd, "Running pytest")

    print("=" * 60)

    if exit_code == 0:
        print("🎉 All tests passed!")

        if args.coverage:
            print("\n📊 Coverage report generated in htmlcov/index.html")

    else:
        print("💥 Some tests failed!")
        print(f"Exit code: {exit_code}")

    # Additional information
    print("\n📝 Test Files:")
    test_files = [
        "test_main.py - Core functionality tests",
        "test_edge_cases.py - Edge cases and error conditions",
        "test_cli.py - Command-line interface tests",
        "test_integration.py - End-to-end integration tests",
    ]
    for test_file in test_files:
        print(f"  • {test_file}")

    print("\n🚀 Quick Commands:")
    print("  python run_tests.py --unit          # Run only unit tests")
    print("  python run_tests.py --coverage      # Run with coverage")
    print("  python run_tests.py --fast          # Quick run")
    print("  python run_tests.py --install-deps  # Install dependencies first")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
