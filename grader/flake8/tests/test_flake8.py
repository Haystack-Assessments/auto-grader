#!/usr/bin/env python3
"""
Purpose:
    Test File for flake8.py
"""

# Python Library Imports
# N/A

# Local Python Library Imports
from grader.flake8.flake8 import Flake8


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


def test_Flake8___init___base() -> int:
    """
    Purpose:
        Test Flake8 Constructor Works
    Args:
        N/A
    Return:
        test_results: 0 for pass, -1 for fail
    Raises:
        N/A
    """

    # Example Data
    test_source_code = "./"

    # Init Flake8
    test_flake8 = Flake8(test_source_code)
    assert test_flake8.source_code == test_source_code
    assert test_flake8.code_dir == f"{test_source_code}"
    assert test_flake8.python_package == "*"
    assert test_flake8.args == [("--max-complexity", 10), ("--max-line-length", 88)]
    assert test_flake8.flags == ["--statistics"]


def test_Flake8___init___override() -> int:
    """
    Purpose:
        Test Flake8 Constructor Works with optional args entered
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

    # Init Flake8
    test_flake8 = Flake8(
        test_source_code,
        python_package=test_python_package,
        args=test_args,
        flags=test_flags,
    )
    assert test_flake8.source_code == test_source_code
    assert test_flake8.python_package == test_python_package
    assert test_flake8.code_dir == f"{test_source_code}/{test_python_package}"
    assert test_flake8.args == test_args
    assert test_flake8.flags == test_flags
