#!/usr/bin/env python3
"""
Purpose:
    Test File for pylint.py
"""

# Python Library Imports
# N/A

# Local Python Library Imports
from grader.pylint.pylint import Pylint


###########
# Mocks/Fixtures
###########


# N/A


###########
# Tests: LinkedList
###########


###
# __init__()
###


def test_Pylint___init___base() -> int:
    """
    Purpose:
        Test Pylint Constructor Works
    Args:
        N/A
    Return:
        test_results: 0 for pass, -1 for fail
    Raises:
        N/A
    """

    # Example Data
    test_source_code = "./"

    # Init Pylint
    test_pylint = Pylint(test_source_code)
    assert test_pylint.source_code == test_source_code
    assert test_pylint.code_dir == f"{test_source_code}"
    assert test_pylint.python_package == "*"
    assert test_pylint.args == [
        ("--output-format", "parseable"),
        ("--ignore", "'./docs .eggs/ .git/ ./venv ./tests'"),
    ]
    assert test_pylint.flags == []


def test_Pylint___init___override() -> int:
    """
    Purpose:
        Test Pylint Constructor Works with optional args entered
    Args:
        N/A
    Return:
        test_results: 0 for pass, -1 for fail
    Raises:
        N/A
    """

    # Example Data
    test_source_code = "./"
    test_python_package = "example"
    test_args = [("test", "true")]
    test_flags = ["--example"]

    # Init Pylint
    test_pylint = Pylint(
        test_source_code,
        python_package=test_python_package,
        args=test_args,
        flags=test_flags,
    )
    assert test_pylint.source_code == test_source_code
    assert test_pylint.python_package == test_python_package
    assert test_pylint.code_dir == f"{test_source_code}/{test_python_package}"
    assert test_pylint.args == test_args
    assert test_pylint.flags == test_flags
