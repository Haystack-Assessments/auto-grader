#!/usr/bin/env python3
"""
Purpose:
    Test File for report_python.py
"""

# Python Library Imports
# N/A

# Local Python Library Imports
from grader.report.report_python import ReportPython


###########
# Mocks/Fixtures
###########


# N/A


###########
# Tests: Report Python
###########


###
# __init__()
###


def test_ReportPython___init___base() -> int:
    """
    Purpose:
        Test ReportPython Constructor Works
    Args:
        N/A
    Return:
        test_results: 0 for pass, -1 for fail
    Raises:
        N/A
    """

    # Example Data
    test_report_name = "test"
    test_candidate_name = "Mr. Test"
    test_source_code = "./"

    # Init ReportPython
    test_report_python = ReportPython(
        test_report_name,
        test_candidate_name,
        test_source_code,
    )
    assert test_report_python.report_name == test_report_name
    assert test_report_python.candidate_name == test_candidate_name
    assert test_report_python.source_code == test_source_code
