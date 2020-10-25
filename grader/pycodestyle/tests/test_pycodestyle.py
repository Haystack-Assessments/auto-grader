#!/usr/bin/env python3
"""
Purpose:
    Test File for pycodestyle.py
"""

# Python Library Imports
# N/A

# Local Python Library Imports
from grader.pycodestyle.pycodestyle import Pycodestyle


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


def test_Pycodestyle___init___base() -> int:
    """
    Purpose:
        Test Pycodestyle Constructor Works
    Args:
        N/A
    Return:
        test_results: 0 for pass, -1 for fail
    Raises:
        N/A
    """

    # Example Data
    test_source_code = "./"

    # Init Pycodestyle
    test_pycodestyle = Pycodestyle(test_source_code)
    assert test_pycodestyle.source_code == test_source_code
    assert test_pycodestyle.code_dir == f"{test_source_code}"
    assert test_pycodestyle.python_package == "*"
    assert test_pycodestyle.args == [("--max-line-length", 88), ("--exclude", "'.eggs tests .venv'")]
    assert test_pycodestyle.flags == ["--statistics"]


def test_Pycodestyle___init___override() -> int:
    """
    Purpose:
        Test Pycodestyle Constructor Works with optional args entered
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

    # Init Pycodestyle
    test_pycodestyle = Pycodestyle(
        test_source_code,
        python_package=test_python_package,
        args=test_args,
        flags=test_flags,
    )
    assert test_pycodestyle.source_code == test_source_code
    assert test_pycodestyle.python_package == test_python_package
    assert test_pycodestyle.code_dir == f"{test_source_code}/{test_python_package}"
    assert test_pycodestyle.args == test_args
    assert test_pycodestyle.flags == test_flags
