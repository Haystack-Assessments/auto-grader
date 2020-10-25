#!/usr/bin/env python3
"""
Purpose:
    Test File for pytest.py
"""

# Python Library Imports
# N/A

# Local Python Library Imports
from grader.pytest.pytest import Pytest


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


def test_Pytest___init___base() -> int:
    """
    Purpose:
        Test Pytest Constructor Works
    Args:
        N/A
    Return:
        test_results: 0 for pass, -1 for fail
    Raises:
        N/A
    """

    # Example Data
    test_source_code = "./"
    test_base_report_path = "./"

    # Init Pytest
    test_pytest = Pytest(test_source_code, test_base_report_path)
    assert test_pytest.source_code == test_source_code
    assert test_pytest.code_dir == f"{test_source_code}"
    assert test_pytest.python_package == "*"
    assert test_pytest.args == [
        ("--maxfail", 999),
        ("--color", "no"),
        ("--code-highlight", "no"),
        ("--cov", "./"),
        ("--html", f"{test_base_report_path}/pytest/index.html"),
        ("--cov-report", f"html:{test_base_report_path}/pytest-cov/"),
        ("--cov-report", "term"),
    ]
    assert test_pytest.flags == ["--doctest-modules", "--self-contained-html", "--verbose"]


def test_Pytest___init___override() -> int:
    """
    Purpose:
        Test Pytest Constructor Works with optional args entered
    Args:
        N/A
    Return:
        test_results: 0 for pass, -1 for fail
    Raises:
        N/A
    """

    # Example Data
    test_source_code = "./"
    test_base_report_path = "./"
    test_python_package = "example"
    test_args = [("test", "true")]
    test_flags = ["--example"]

    # Init Pytest
    test_pytest = Pytest(
        test_source_code,
        test_base_report_path,
        python_package=test_python_package,
        args=test_args,
        flags=test_flags,
    )
    assert test_pytest.source_code == test_source_code
    assert test_pytest.python_package == test_python_package
    assert test_pytest.code_dir == f"{test_source_code}/{test_python_package}"
    assert test_pytest.args == test_args
    assert test_pytest.flags == test_flags
