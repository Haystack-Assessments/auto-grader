#!/usr/bin/env python3
"""
Purpose:
    ReportPython Class Definition

    Hold the implementation of the report for a python project
"""

# Python Library Imports
import os
import pathlib
from typing import Any, Dict

# Local Python Library Imports
import grader.subprocess.subprocess as subprocess
from grader.artifacts.report_templates.report_python import report_python_template
from grader.flake8.flake8 import Flake8
from grader.mypy.mypy import Mypy
from grader.pytest.pytest import Pytest
from grader.pylint.pylint import Pylint
from grader.pycodestyle.pycodestyle import Pycodestyle


###
# Class Definition
###


class ReportPython:
    """
    Purpose:
        The ReportPython Class represents a python grade report for code
    """

    report_summary_template = report_python_template

    ###
    # Reserved Methods
    ###

    def __init__(
        self,
        report_name: str,
        candidate_name: str,
        source_code: str,
        base_report_path: str = f"{os.path.abspath('./')}/reports",
    ) -> None:
        """
        Purpose:
            Constructor for a ReportPython
        Args:
            report_name: unique name for the report
            candidate_name: name of the candidate
            source_code: path to the code to grade
            base_report_path: path to reports to save. Defaults to ./reports
        Returns:
            N/A
        Raises:
            Exception: If the path to code is not valid
        """

        if not os.path.isdir(source_code):
            raise Exception(f"{source_code} is not a valid path to code")

        self.base_report_path = base_report_path
        self.source_code = source_code
        self.report_name = report_name
        self.candidate_name = candidate_name

    def __repr__(self) -> None:
        """
        Purpose:
            String Representation for a ReportPython
        Args:
            N/A
        Returns:
            N/A
        Raises:
            N/A
        """

        return f"<ReportPython {self.report_name} (of {self.source_code})>"

    ###
    # Properties
    ###

    @property
    def report_path(self):
        """
        Purpose:
            Get the path to the report
        Args:
            N/A
        Returns:
            N/A
        Raises:
            N/A
        """

        return f"{self.base_report_path}/{self.report_name}"

    @property
    def report_summary_path(self):
        """
        Purpose:
            Get the
        Args:
            N/A
        Returns:
            N/A
        Raises:
            N/A
        """

        return f"{self.report_path}/report_summary.md"

    ###
    # Report Operations
    ###

    def generate_report(self, overwrite: bool = False) -> None:
        """
        Purpose:
            Generate the Full Report

            If overwrite is false and report exists, will fail
        Args:
            N/A
        Returns:
            N/A
        Raises:
            Exception: if report exists and overwrite is false
        """

        if os.path.isdir(self.report_path) and not overwrite:
            raise Exception(f"Report {self.report_name} already exists")

        pathlib.Path(self.report_path).mkdir(parents=True, exist_ok=True)

        report_data = self.get_report_data()

        report_summary_data = self.build_report_summary(report_data)

        self.store_report_summary(report_summary_data)

    def get_report_data(self) -> Dict[str, Any]:
        """
        Purpose:
            Gather Data for the report. Will run each component and get parsed data
        Args:
            N/A
        Returns:
            report_data: Dict of parsed and formatted report data
        Raises:
            Exception: if any of the report components fail
        """

        # Set Up Runners
        flake8_runner = Flake8(self.source_code)
        mypy_runner = Mypy(self.source_code)
        pylint_runner = Pylint(self.source_code)
        pytest_runner = Pytest(self.source_code, self.report_path)
        pycodestyle_runner = Pycodestyle(self.source_code)

        report_data = {
            "candidate": {"name": self.candidate_name},
            "flake8": flake8_runner.run(),
            "mypy": mypy_runner.run(),
            "pylint": pylint_runner.run(),
            "pytest": pytest_runner.run(),
            "pycodestyle": pycodestyle_runner.run(),
        }

        return report_data

    def build_report_summary(self, report_data: Dict[str, Any]) -> str:
        """
        Purpose:
            Store the finalize Report
        Args:
            report_data: Dict of parsed and formatted report data
        Returns:
            report_summary: formatted report summary
        Raises:
            Exception: if report storing fails
        """

        return self.report_summary_template.format(**report_data)

    def store_report_summary(self, report_summary: str) -> None:
        """
        Purpose:
            Store the finalize Report
        Args:
            N/A
        Returns:
            N/A
        Raises:
            Exception: if report storing fails
        """

        with open(self.report_summary_path, "w") as report_summary_file_obj:
            report_summary_file_obj.write(report_summary)
