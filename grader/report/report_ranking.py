#!/usr/bin/env python3
"""
Purpose:
    ReportRanking Class Definition

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
from grader.artifacts.report_templates.report_ranking import report_ranking_html_template


###
# Class Definition
###


class ReportRanking:
    """
    Purpose:
        The ReportRanking Class represents a python grade report for code
    """

    ###
    # Class Attributes
    ###

    max_graph_columns = 3

    ###
    # Reserved Methods
    ###

    def __init__(
        self,
        report_name: str,
        candidate_path: str,
        base_report_path: str = f"{os.path.abspath('./')}/reports/ranking",
    ) -> None:
        """
        Purpose:
            Constructor for a ReportRanking
        Args:
            report_name: unique name for the report
            candidate_path: path to candidate reports to rank
            base_report_path: path to reports to save. Defaults to ./reports/ranking
        Returns:
            N/A
        Raises:
            Exception: If the path to code is not valid
        """

        # Report Data
        self.base_report_path = base_report_path
        self.report_name = report_name

        if not candidate_path:
            self.candidate_path = f"{os.path.abspath('./')}/reports/python_candidates"
        else:
            # Validate Code Dir Exists
            if not os.path.isdir(candidate_path):
                raise Exception(
                    f"{candidate_path} is not a valid path to candidate reports"
                )
            self.candidate_path = candidate_path

        # Candidate Data
        self.candidates = {}

    def __repr__(self) -> None:
        """
        Purpose:
            String Representation for a ReportRanking
        Args:
            N/A
        Returns:
            N/A
        Raises:
            N/A
        """

        return (
            f"<ReportRanking {self.report_name} (of {self.candidate_path})>"
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
    def report_md_summary_path(self):
        """
        Purpose:
            Markdown Summary Filename
        Args:
            N/A
        Returns:
            report_md_summary_path: name of the .md summary file that is stored
        Raises:
            N/A
        """

        return f"{self.report_path}/report_summary.md"

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

        # Load all Candidate Data
        self.load_candidate_data()

        # Build Assets
        self.build_report_assets()

        # Get Pure Report Data
        report_data = self.get_report_data()
        # Store Data
        self.store_report_summary(report_data)

    ###
    # Compile Data Operations
    ###

    def load_candidate_data(self) -> None:
        """
        Purpose:
            Loads all found candidate data
        Args:
            N/A
        Returns:
            report_data: Dict of parsed and formatted report data
        Raises:
            Exception: if any of the report components fail
        """

        candidate_report_data_files = [
            f"{self.candidate_path}/{candidate_report}/report_raw_data.json"
            for candidate_report
            in os.listdir(self.candidate_path)
            if (
                os.path.isdir(f"{self.candidate_path}/{candidate_report}")
                and os.path.isfile(
                    f"{self.candidate_path}/{candidate_report}/report_raw_data.json"
                )
            )
        ]

        for candidate_report_data_file in candidate_report_data_files:
            try:
                with open(candidate_report_data_file, "r") as report_data_file_obj:
                    candidate_data = json.load(report_data_file_obj)
                    candidate_name = candidate_data["candidate"]["name"]

                    if candidate_name in self.candidates:
                        raise Exception(
                            f"{candidate_name} is duplicated, check candidate source"
                        )

                    self.candidates[candidate_name] = candidate_data
            except Exception as err:
                continue

    def get_report_data(self) -> Dict[str, Any]:
        """
        Purpose:
            Gather Data for the report. Will build basic data
        Args:
            N/A
        Returns:
            report_data: Dict of parsed and formatted report data
        Raises:
            Exception: if gathering data fails
        """

        # Convert Candidates into HTML Unordered List
        candidate_list_html = "<ul class='candidates'>"
        for candidate in self.candidates.values():
            candidate_list_html += f"<li>{candidate['candidate']['name']}</li>"
        candidate_list_html += f"</ul>"

        report_data = {
            "candidate_list_html": candidate_list_html,
        }

        return report_data

    ###
    # Graph/Chart Operations
    ###

    def build_report_assets(self) -> None:
        """
        Purpose:
            Build assets for the report. includes all graphs and charts
        Args:
            N/A
        Returns:
            N/A
        Raises:
            Exception: If buliding any asset fails
        """

        self.build_error_count_line_charts()
        self.build_pylint_scores_bar_chart()
        self.build_test_breakdown_pie_charts()

    def build_error_count_line_charts(self) -> None:
        """
        Purpose:
            Build Error Count Line Charts each candidate. Store a single image in
            assets
        Args:
            N/A
        Returns:
            N/A
        Raises:
            Exception: if graph building fails
        """

        # Get data for chart
        df_errors_by_tool = pd.DataFrame.from_dict(
            self.compile_errors_by_tool(), orient="index"
        )

        # Get Candidate Rows for multiplot, will do n-wide columns
        candidate_rows = math.ceil(len(self.candidates) / self.max_graph_columns)

        # Create the Figure
        fig = plt.figure()

        # Initialize the figure style
        plt.style.use("seaborn-darkgrid")

        # Setting Dark2 Color Pallet, easier to read
        palette = plt.get_cmap("Dark2")

        # Find Max value for y-axis
        max_errors = 0
        for candidate in df_errors_by_tool.drop("tool", axis=1):
            if max(df_errors_by_tool[candidate]) > max_errors:
                max_errors = max(df_errors_by_tool[candidate])
        max_errors = math.ceil(max_errors * 1.05)  # adding 5% to max num for graph

        # Iterate through each candidate to build a plot
        for idx, tool in enumerate(df_errors_by_tool.drop("tool", axis=1)):

            # Add a subplot
            subplot = fig.add_subplot(
                self.max_graph_columns, candidate_rows, idx + 1
            )

            # Plot the lineplot
            subplot.plot(
                df_errors_by_tool["tool"],
                df_errors_by_tool[tool],
                marker="",
                color=palette(idx + 1),
                linewidth=1.9,
                alpha=0.9,
                label=tool
            )

            # Set Max for the subplot
            plt.ylim(0, max_errors)

            # Add titles to subplot
            plt.title(
                tool,
                loc="left",
                fontsize=12,
                fontweight=0,
                color=palette(idx + 1)
            )
            plt.xticks(rotation=15)

        # Create Spacing for each subplot
        fig.subplots_adjust(right=2, top=3, wspace=.2, hspace=.6)

        # Resize Plot to fit everything
        plt.tight_layout()

        # Store the figure
        fig.savefig(f"{self.asset_path}/error_count_line_charts.png")

        # Close Plot
        plt.close()

    def compile_errors_by_tool(self) -> Dict[str, Dict[str, Any]]:
        """
        Purpose:
            Compile a dict of error for each tool to graph the results
        Args:
            N/A
        Returns:
            errors_by_tool: Dict where a key is a tool and then each candidates results
                for that tool are stored
        Raises:
            Exception: if compiling data fails
        """

        errors_by_tool = {
            "pylint": {"tool": "pylint"},
            "flake8": {"tool": "flake8"},
            "pycodestyle": {"tool": "pycodestyle"},
            "mypy": {"tool": "mypy"},
        }

        for candidate in self.candidates.values():
            candidate_name = candidate["candidate"]["name"]
            errors_by_tool["mypy"][candidate_name] = \
                candidate["mypy"]["metrics"]["total"]
            errors_by_tool["pylint"][candidate_name] = \
                candidate["pylint"]["metrics"]["total"]
            errors_by_tool["pycodestyle"][candidate_name] = \
                candidate["pycodestyle"]["metrics"]["total"]
            errors_by_tool["flake8"][candidate_name] = \
                candidate["flake8"]["metrics"]["total"]

        return errors_by_tool

    def build_pylint_scores_bar_chart(self) -> None:
        """
        Purpose:
            Build Pylint Score Bar chart with each candidates data
        Args:
            N/A
        Returns:
            N/A
        Raises:
            Exception: if graph building fails
        """

        # Get data for chart
        df_pylint_scores_by_cadidate = pd.DataFrame.from_dict(
            self.compile_pylint_scores_by_cadidate(), orient="index"
        )

        # Sort Values
        df_pylint_scores_by_cadidate = df_pylint_scores_by_cadidate.sort_values(
            by=["pylint_score"], ascending=False
        )

        # Create Bar Chart
        df_pylint_scores_by_cadidate.plot.bar(rot=0)

        # Chart Title
        plt.suptitle(
            "Pylint Scores By Candidate",
            fontsize=13,
            fontweight=0,
            color='black',
            style='italic',
            y=.95
        )

        # Axis title
        plt.xticks(rotation=10)

        # Store the figure
        plt.savefig(f"{self.asset_path}/pylint_scores_by_candidate.png")

        # Close Plot
        plt.close()

    def compile_pylint_scores_by_cadidate(self) -> Dict[str, Dict[str, Any]]:
        """
        Purpose:
            Compile a dict of pylint scores for each candidate
        Args:
            N/A
        Returns:
            pylint_score_by_candidate: Dict where a key is a candidate and the
                the value is the pylint score
        Raises:
            Exception: if compiling data fails
        """

        pylint_score_by_candidate = {
            candidate["candidate"]["name"]: {
                "name": candidate["candidate"]["name"],
                "pylint_score": float(candidate["pylint"]["score"]),
            }
            for candidate
            in self.candidates.values()
        }

        return pylint_score_by_candidate

    def build_test_breakdown_pie_charts(self) -> None:
        """
        Purpose:
            Build Test Breakdown Pie Charts for each candidate. Store a single image in
            assets
        Args:
            N/A
        Returns:
            N/A
        Raises:
            Exception: if graph building fails
        """

        # Get data for chart
        test_success_by_cadidate = self.compile_test_success_by_cadidate()

        # Get Candidate Rows for multiplot, will do n-wide columns
        candidate_rows = math.ceil(len(self.candidates) / self.max_graph_columns)

        # Create the Figure
        fig = plt.figure()

        # Iterate through each candidate
        idx = 0
        for candidate, test_scores in test_success_by_cadidate.items():

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

            # Add a subplot
            subplot = fig.add_subplot(
                self.max_graph_columns, candidate_rows, idx + 1
            )

            # Add Pie Chart
            subplot.pie(
                result_percentages,
                labels=test_results,
                autopct='%1.1f%%',
                shadow=True,
                startangle=90,
                colors=slice_colors,
            )
            subplot.axis("equal")

            # Add titles to subplot
            plt.title(
                candidate,
                loc="center",
                fontsize=12,
                fontweight=0,
            )

            idx += 1

        # Create Spacing for each subplot
        fig.subplots_adjust(right=2, top=3, wspace=.2, hspace=.6)

        # Resize Plot to fit everything
        plt.tight_layout()

        # Store the figure
        fig.savefig(f"{self.asset_path}/test_breakdown_pie_charts.png")

        # Close Plot
        plt.close()

    def compile_test_success_by_cadidate(self) -> Dict[str, Dict[str, Any]]:
        """
        Purpose:
            Compile a dict of test success/fail by candidate
        Args:
            N/A
        Returns:
            test_success_by_cadidate: Dict where a key is a candidate and the
                success/fail is broken down by percentage
        Raises:
            Exception: if compiling data fails
        """

        test_success_by_cadidate = {
            candidate["candidate"]["name"]: {
                "percentage_error":
                    candidate["pytest"]["tests"]["metrics"]["percentage_error"],
                "percentage_failed":
                    candidate["pytest"]["tests"]["metrics"]["percentage_failed"],
                "percentage_passed":
                    candidate["pytest"]["tests"]["metrics"]["percentage_passed"],
            }
            for candidate
            in self.candidates.values()
        }

        return test_success_by_cadidate

    ###
    # Store Operations
    ###

    def store_report_summary(self, report_data: Dict[str, Any]) -> None:
        """
        Purpose:
            Store the finalize Report in .html and .md for consumption
        Args:
            report_data: Dict of parsed and formatted report data
        Returns:
            N/A
        Raises:
            Exception: if report storing fails
        """

        with open(self.report_html_summary_path, "w") as report_html_summary_file_obj:
            report_html_summary_file_obj.write(
                report_ranking_html_template.format(**report_data)
            )
