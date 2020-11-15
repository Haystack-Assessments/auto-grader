#!/usr/bin/env python3
"""
Purpose:
    ReportPython Class Definition

    Hold the implementation of the report for a python project
"""

# Python Library Imports
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pathlib
from typing import Any, Dict

# Local Python Library Imports
import grader.subprocess.subprocess as subprocess
from grader.artifacts.report_templates.report_python import report_python_html_template
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

    ###
    # Reserved Methods
    ###

    def __init__(
        self,
        report_name: str,
        candidate_name: str,
        source_code: str,
        python_package: str = None,
        base_report_path: str = f"{os.path.abspath('./')}/reports/python_candidates",
    ) -> None:
        """
        Purpose:
            Constructor for a ReportPython
        Args:
            report_name: unique name for the report
            candidate_name: name of the candidate
            source_code: path to the code to grade
            python_package: package to assess, defaults to *
            base_report_path: path to reports to save. Defaults to ./reports
        Returns:
            N/A
        Raises:
            Exception: If the path to code is not valid
        """

        # Code Data
        self.source_code = source_code
        if python_package:
            self.code_dir = f"{source_code}/{python_package}"
            self.python_package = python_package
        else:
            self.code_dir = source_code
            self.python_package = "*"

        # Report Data
        self.base_report_path = base_report_path
        self.report_name = report_name
        self.candidate_name = candidate_name

        # Validate Code Dir Exists
        if not os.path.isdir(self.code_dir):
            raise Exception(f"{self.code_dir} is not a valid path to code")

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

        return (
            f"<ReportPython {self.report_name} (of "
            f"{self.source_code}/{python_package})>"
        )

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
            report_path: Path where all data is stored
        Raises:
            N/A
        """

        return f"{self.base_report_path}/{self.report_name}"

    @property
    def asset_path(self):
        """
        Purpose:
            Get the path to the assets for the report
        Args:
            N/A
        Returns:
            report_path: Path where all assets is stored
        Raises:
            N/A
        """

        return f"{self.report_path}/assets/"

    @property
    def report_html_summary_path(self):
        """
        Purpose:
            HTML Summary Filename
        Args:
            N/A
        Returns:
            report_html_summary_path: name of the .html summary file that is stored
        Raises:
            N/A
        """

        return f"{self.report_path}/report_summary.html"

    @property
    def report_raw_data_path(self):
        """
        Purpose:
            Raw Data Filename
        Args:
            N/A
        Returns:
            report_raw_data_path: name of the raw data file that is stored
        Raises:
            N/A
        """

        return f"{self.report_path}/report_raw_data.json"

    ###
    # Report Operations
    ###

    def generate_report(self, overwrite: bool = False) -> None:
        """
        Purpose:
            Generate the Full Report

            If overwrite is false and report exists, will fail
        Args:
            overwrite: whether or not to overwrite the file if it already exists
        Returns:
            N/A
        Raises:
            Exception: if report exists and overwrite is false
        """

        # Ensuring path doesn't already exist
        if os.path.isdir(self.report_path) and not overwrite:
            raise Exception(f"Report {self.report_name} already exists")

        # Create the path
        pathlib.Path(self.report_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.asset_path).mkdir(parents=True, exist_ok=True)

        # Get Pure Report Data
        report_data = self.get_report_data()

        # Build Assets
        self.build_report_assets(report_data)

        # Store Data
        self.store_report_summary(report_data)
        self.store_report_raw_data(report_data)

    ###
    # Compile Data Operations
    ###

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
        flake8_runner = Flake8(self.source_code, python_package=self.python_package)
        mypy_runner = Mypy(self.source_code, python_package=self.python_package)
        pylint_runner = Pylint(self.source_code, python_package=self.python_package)
        pytest_runner = Pytest(
            self.source_code, self.report_path, python_package=self.python_package
        )
        pycodestyle_runner = Pycodestyle(
            self.source_code, python_package=self.python_package
        )

        report_data = {
            "candidate": {"name": self.candidate_name},
            "flake8": flake8_runner.run(),
            "mypy": mypy_runner.run(),
            "pylint": pylint_runner.run(),
            "pytest": pytest_runner.run(),
            "pycodestyle": pycodestyle_runner.run(),
        }

        return report_data

    ###
    # Graph/Chart Operations
    ###

    def build_report_assets(self, report_data: Dict[str, Any]) -> None:
        """
        Purpose:
            Build assets for the report. includes all graphs and charts
        Args:
            report_data: Dict of parsed and formatted report data
        Returns:
            N/A
        Raises:
            Exception: If buliding any asset fails
        """

        self.build_error_count_line_chart(report_data)
        self.build_test_breakdown_pie_chart(report_data)

    def build_error_count_line_chart(self, report_data: Dict[str, Any]) -> None:
        """
        Purpose:
            Build Error Count Line Charts each candidate. Store a single image in
            assets
        Args:
            report_data: Dict of parsed and formatted report data
        Returns:
            N/A
        Raises:
            Exception: if graph building fails
        """

        # Initialize the figure style
        plt.style.use("seaborn-darkgrid")

        # Plot the scores as line chart
        plt.plot(
            ["pylint", "flake8", "pycodestyle", "mypy"],
            [
                report_data["pylint"]["metrics"]["total"],
                report_data["flake8"]["metrics"]["total"],
                report_data["pycodestyle"]["metrics"]["total"],
                report_data["mypy"]["metrics"]["total"],
            ]
        )

        # Store the figure
        plt.savefig(f"{self.asset_path}/error_count_line_chart.png")

        # Clost Plot
        plt.close()

    def build_test_breakdown_pie_chart(self, report_data: Dict[str, Any]) -> None:
        """
        Purpose:
            Build Test Breakdown Pie Chart. Store a single image in assets
        Args:
            report_data: Dict of parsed and formatted report data
        Returns:
            N/A
        Raises:
            Exception: if graph building fails
        """

        test_scores = {
            "percentage_error":
                report_data["pytest"]["tests"]["metrics"]["percentage_error"],
            "percentage_failed":
                report_data["pytest"]["tests"]["metrics"]["percentage_failed"],
            "percentage_passed":
                report_data["pytest"]["tests"]["metrics"]["percentage_passed"],
        }

        test_results = []
        result_percentages = []
        slice_colors = []
        # Getting data to chart (different depending on results, e.g. no fails)
        for test_result, percentage in test_scores.items():

            # Only add result if >0 for cleaner graphs
            if percentage > 0:
                test_results.append(test_result.replace("percentage_", ""))
                result_percentages.append(percentage)
                if "passed" in test_result:
                    slice_colors.append("green")
                else:
                    slice_colors.append("red")

        # Add Pie Chart
        plt.pie(
            result_percentages,
            labels=test_results,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90,
            colors=slice_colors,
        )
        plt.axis("equal")

        # Add titles to subplot
        plt.title(
            "Test Results",
            loc="center",
            fontsize=12,
            fontweight=0,
        )

        # Store the figure
        plt.savefig(f"{self.asset_path}/test_breakdown_pie_chart.png")

        # Clost Plot
        plt.close()

    ###
    # Store Operations
    ###

    def store_report_summary(self, report_data: Dict[str, Any]) -> None:
        """
        Purpose:
            Store the finalize Report in .html for consumption
        Args:
            report_data: Dict of parsed and formatted report data
        Returns:
            N/A
        Raises:
            Exception: if report storing fails
        """

        with open(self.report_html_summary_path, "w") as report_html_summary_file_obj:
            report_html_summary_file_obj.write(
                report_python_html_template.format(**report_data)
            )

    def store_report_raw_data(self, report_data: Dict[str, Any]) -> None:
        """
        Purpose:
            Store the raw data
        Args:
            report_data: Dict of parsed and formatted report data
        Returns:
            N/A
        Raises:
            Exception: if report storing fails
        """

        with open(self.report_raw_data_path, "w") as report_raw_data_file_obj:
            json.dump(
                report_data,
                report_raw_data_file_obj,
                sort_keys=True,
                indent=2,
                separators=(",", ": "),
            )
