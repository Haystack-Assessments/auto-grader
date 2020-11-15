#!/usr/bin/env python3
"""
Purpose:
    Test File for report_rank.py
"""

# Python Library Imports
# N/A

# Local Python Library Imports
from grader.report.report_ranking import ReportRanking


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


def test_ReportRanking___init___base() -> int:
    """
    Purpose:
        Test ReportRanking Constructor Works
    Args:
        N/A
    Return:
        test_results: 0 for pass, -1 for fail
    Raises:
        N/A
    """

    # Example Data
    test_report_name = "test"
    test_candidate_path = "./"

    # Init ReportRanking
    test_ranking_report = ReportRanking(
        test_report_name,
        test_candidate_path
    )
    assert test_ranking_report.report_name == test_report_name
    assert test_ranking_report.candidate_path == test_candidate_path
