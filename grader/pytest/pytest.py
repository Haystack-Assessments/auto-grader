"""
Purpose:
    Pytest Class Definition

    Responsible for interacting with Pytest
"""

# Python Library Imports
import os
import re
from typing import Any, Dict, List, Optional, Union

# Local Python Library Imports
import grader.subprocess.subprocess as subprocess
from grader.tool.tool import Tool


###
# Class Definition
###


class Pytest(Tool):
    """
    Purpose:
        Responsible for interacting with Pytest
    """

    default_args = [
        ("--maxfail", 999),
        ("--color", "no"),
        ("--code-highlight", "no"),
        ("--cov", "./"),
    ]
    default_flags = ["--doctest-modules", "--self-contained-html", "--verbose"]

    ###
    # Reserved Methods
    ###

    def __init__(
        self,
        source_code: str,
        base_report_path: str,
        python_package: str = None,
        args: Optional[Dict[str, str]] = None,
        flags: Optional[List[str]] = None,
    ) -> None:
        """
        Purpose:
            Constructor for a Mypy
        Args:
            source_code: code to run mypy on
            python_package: python_package to assess
            base_report_path: path to store reports
            args: argument overrides for mypy
            flags: flag overrides for mypy
        Returns:
            N/A
        Raises:
            Exception: If the path to code is not valid
        """

        super().__init__(
            source_code,
            python_package=python_package,
            args=args,
            flags=flags,
        )

        # Add Report Path for Storing Results
        self.base_report_path = base_report_path

        # Add Extra Args for Pytest
        self.args.append(("--html", f"{self.base_report_path}/pytest/index.html"))
        self.args.append(("--cov-report", f"html:{self.base_report_path}/pytest-cov/"))
        self.args.append(("--cov-report", "term"))

    def __repr__(self) -> str:
        """
        Purpose:
            String Representation for a Pytest
        Args:
            N/A
        Returns:
            pytest_repr: command that will be run
        Raises:
            N/A
        """

        return f"<Pytest {self.command})>"

    ###
    # Properties
    ###

    @property
    def command(self):
        """
        Purpose:
            Get the Pytest command
        Args:
            N/A
        Returns:
            N/A
        Raises:
            N/A
        """

        parsed_args = " ".join([f"{arg}={value}" for (arg, value) in self.args])
        parsed_flags = " ".join(self.flags)

        return f"python3 -m pytest {parsed_flags} {parsed_args}"

    ###
    # Pytest Operations
    ###

    def run(self) -> Dict[str, Any]:
        """
        Purpose:
            Run Pytest tool against the target code
        Args:
            N/A
        Returns:
            pytest_stdout: parsed output from pytest
        Raises:
            N/A
        """

        # Run Pytest command with pexpect and capture output
        (raw_pytest_stdout, _) = subprocess.run_subprocess_call(
            command=self.command, env={}, cwd=self.source_code, timeout=60
        )

        return self._parse_output(raw_pytest_stdout)

    def _parse_output(self, raw_pytest_stdout: bytes) -> Dict[str, Any]:
        """
        Purpose:
            Parse the Pytest output to get standarized results for reporting
        Args:
            raw_pytest_stdout: raw output from the pytest command
        Returns:
            N/A
        Raises:
            N/A
        """

        # Set up return objects
        parsed_output = {
            "tests": {
                "metrics": {"error_tests": 0, "passed_tests": 0, "failed_tests": 0},
                "error_tests": [],
                "passed_tests": [],
                "failed_tests": [],
                "summary": "",
            },
            "coverage": {"metrics": {}, "details": [], "summary": ""},
        }

        # Set up Regex for parsing
        fatal_test_regex = r".*ModuleNotFoundError"
        error_test_regex = r".*ERROR"
        passed_test_regex = r".*PASSED +\[[ 0-9]{3}\%\]"
        failed_test_regex = r".*FAILED +\[[ 0-9]{3}\%\]"
        coverage_details_regex = r".*\.py.*\d{1,3}\%$"
        coverage_totals_regex = r"TOTAL.*\d{1,3}\%$"

        for output_line in raw_pytest_stdout:

            if re.match(fatal_test_regex, output_line):
                raise Exception(f"Pytest Cannot run without modules: {output_line}")

            # Getting the Message Type
            message_type = None
            if re.match(error_test_regex, output_line):
                message_type = "error_tests"
            elif re.match(passed_test_regex, output_line):
                message_type = "passed_tests"
            elif re.match(failed_test_regex, output_line):
                message_type = "failed_tests"
            elif re.match(coverage_details_regex, output_line):
                message_type = "coverage_details"
            elif re.match(coverage_totals_regex, output_line):
                message_type = "coverage_totals"

            # Updating Report
            if not message_type:
                # non-matching line
                continue
            if message_type in ("error_tests", "passed_tests", "failed_tests"):
                # If a test, add to passed/failed
                parsed_output["tests"]["metrics"][message_type] += 1
                parsed_output["tests"][message_type].append(output_line)
            if message_type == "coverage_details":
                # If code coverage for a file, add to coverage details
                parsed_output["coverage"]["details"].append(output_line)
            if message_type == "coverage_totals":
                # If code coverage total, add as summary and to metrics
                parsed_output["coverage"]["metrics"] = self.parse_code_coverage_line(
                    output_line
                )
                parsed_output["coverage"]["summary"] = output_line
            else:
                # non-matching line
                continue

        # Calculate Percentages
        parsed_output["tests"]["metrics"]["total_tests"] = (
            parsed_output["tests"]["metrics"]["failed_tests"]
            + parsed_output["tests"]["metrics"]["passed_tests"]
            + parsed_output["tests"]["metrics"]["error_tests"]
        )
        if parsed_output["tests"]["metrics"]["total_tests"] > 0:
            for test_status in ("error", "failed", "passed"):
                parsed_output["tests"]["metrics"][f"percentage_{test_status}"] = (
                    parsed_output["tests"]["metrics"][f"{test_status}_tests"]
                    / parsed_output["tests"]["metrics"]["total_tests"]
                ) * 100
        else:
            for test_status in ("error", "failed", "passed"):
                parsed_output["tests"]["metrics"][f"percentage_{test_status}"] = 0

        # Stringify Test Items for Reporting
        for message_type in ("error_tests", "passed_tests", "failed_tests"):
            parsed_output["tests"][f"{message_type}_str"] = "\n".join(
                parsed_output["tests"][message_type]
            )

        # Stringify Coverage Items for Reporting
        parsed_output["coverage"]["details_str"] = "\n".join(
            parsed_output["coverage"]["details"]
        )

        return parsed_output

    @staticmethod
    def parse_code_coverage_line(output_line) -> Dict[str, Union[int, float]]:
        """
        Purpose:
            Parse the pytest-cov output line to a Dict
        Args:
            output_line: raw output to parse
        Returns:
            code_coverage: Code coverage details
        Raises:
            N/A
        """

        coverage_tokens = re.findall(r"\d+", output_line)

        if len(coverage_tokens) == 5:
            return {
                "statements_total": coverage_tokens[0],
                "statements_missing": coverage_tokens[1],
                "statements_branching": coverage_tokens[2],
                "statements_partial_branching": coverage_tokens[3],
                "statements_percentage": coverage_tokens[4],
            }
        elif len(coverage_tokens) == 3:
            return {
                "statements_total": coverage_tokens[0],
                "statements_missing": coverage_tokens[1],
                "statements_branching": 0,
                "statements_partial_branching": 0,
                "statements_percentage": coverage_tokens[2],
            }
        else:
            return {
                "statements_total": 0,
                "statements_missing": 0,
                "statements_branching": 0,
                "statements_partial_branching": 0,
                "statements_percentage": 0.0,
            }
