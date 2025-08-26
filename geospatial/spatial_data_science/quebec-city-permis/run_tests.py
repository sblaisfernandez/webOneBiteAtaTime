#!/usr/bin/env python3
"""
Test runner script for utils.py unit tests
"""
import os
import sys
import subprocess


def run_tests():
    """Run the unit tests"""
    print("=" * 60)
    print("Running Unit Tests for utils.py")
    print("=" * 60)

    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    # Run tests with different options
    test_commands = [
        {
            "name": "Basic Tests",
            "cmd": ["python", "-m", "unittest", "test_utils.py", "-v"],
        },
        {
            "name": "Tests with Coverage (if pytest-cov is available)",
            "cmd": [
                "python",
                "-m",
                "pytest",
                "test_utils.py",
                "--cov=utils",
                "--cov-report=html",
                "--cov-report=term-missing",
                "-v",
            ],
        },
        {
            "name": "Tests with Pytest (if pytest is available)",
            "cmd": ["python", "-m", "pytest", "test_utils.py", "-v"],
        },
    ]

    for test_config in test_commands:
        print(f"\n{'-' * 40}")
        print(f"Running: {test_config['name']}")
        print(f"Command: {' '.join(test_config['cmd'])}")
        print(f"{'-' * 40}")

        try:
            result = subprocess.run(test_config["cmd"], capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ PASSED")
                print(result.stdout)
            else:
                print("❌ FAILED")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)

        except FileNotFoundError:
            print(f"⚠️  Command not found: {test_config['cmd'][0]}")
        except Exception as e:
            print(f"❌ Error running test: {e}")

    print("\n" + "=" * 60)
    print("Test run completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
