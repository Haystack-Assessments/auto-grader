#!/usr/bin/env python3
"""
Purpose:
    Test File for mypy.py
"""

# Python Library Imports
# N/A

# Local Python Library Imports
from grader.mypy.mypy import Mypy


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


def test_Mypy___init___base() -> int:
    """
    Purpose:
        Test Mypy Constructor Works
    Args:
        N/A
    Return:
        test_results: 0 for pass, -1 for fail
    Raises:
        N/A
    """

    # Example Data
    test_source_code = "./"

    # Init Mypy
    test_mypy = Mypy(test_source_code)
    assert test_mypy.source_code == test_source_code
    assert test_mypy.code_dir == f"{test_source_code}"
    assert test_mypy.python_package == "*"
    assert test_mypy.args == []
    assert test_mypy.flags == [
        "--disallow-untyped-defs",
        "--disallow-untyped-calls",
        "--disallow-incomplete-defs",
        "--ignore-missing-imports",
        "--namespace-packages",
        "--no-color-output",
    ]


def test_Mypy___init___override() -> int:
    """
    Purpose:
        Test Mypy Constructor Works with optional args entered
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

    # Init Mypy
    test_mypy = Mypy(
        test_source_code,
        python_package=test_python_package,
        args=test_args,
        flags=test_flags,
    )
    assert test_mypy.source_code == test_source_code
    assert test_mypy.python_package == test_python_package
    assert test_mypy.code_dir == f"{test_source_code}/{test_python_package}"
    assert test_mypy.args == test_args
    assert test_mypy.flags == test_flags
