"""
Purpose:
    Pylint Class Definition

    Responsible for interacting with Pylint
"""

# Python Library Imports
import os
import re
from typing import Any, Dict, List, Optional

# Local Python Library Imports
import grader.subprocess.subprocess as subprocess
from grader.tool.tool import Tool


###
# Class Definition
###


class Pylint(Tool):
    """
    Purpose:
        Responsible for interacting with Pylint
    """

    default_args = [
        ("--output-format", "parseable"),
        ("--ignore", "'./docs .eggs/ .git/ ./venv ./tests'"),
    ]
    default_flags = []

    ###
    # Reserved Methods
    ###

    def __init__(
        self,
        source_code: str,
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
            args: argument overrides for mypy
            flags: flag overrides for mypy
        Returns:
            N/A
        Raises:
            Exception: If the path to code is not valid
        """

        super().__init__(
            source_code, python_package=python_package, args=args, flags=flags
        )

    def __repr__(self) -> str:
        """
        Purpose:
            String Representation for a Pylint
        Args:
            N/A
        Returns:
            pylint_repr: command that will be run
        Raises:
            N/A
        """

        return f"<Pylint {self.command})>"

    ###
    # Properties
    ###

    @property
    def command(self):
        """
        Purpose:
            Get the Pylint command
        Args:
            N/A
        Returns:
            N/A
        Raises:
            N/A
        """

        parsed_args = " ".join([f"{arg}={value}" for (arg, value) in self.args])
        parsed_flags = " ".join(self.flags)

        return f"python3 -m pylint {parsed_flags} {parsed_args} {self.python_package}"

    ###
    # Pylint Operations
    ###

    def run(self) -> Dict[str, Any]:
        """
        Purpose:
            Run Pylint tool against the target code
        Args:
            N/A
        Returns:
            pylint_stdout: parsed output from pylint
        Raises:
            N/A
        """

        # Run Pylint command with pexpect and capture output
        (raw_pylint_stdout, _) = subprocess.run_subprocess_call(
            command=self.command,
            env={"PYTHONPATH": self.source_code},
            cwd=self.source_code,
            timeout=60,
        )

        return self._parse_output(raw_pylint_stdout)

    def _parse_output(self, raw_pylint_stdout: bytes) -> Dict[str, Any]:
        """
        Purpose:
            Parse the Pylint output to get standarized results for reporting
        Args:
            raw_pylint_stdout: raw output from the pylint command
        Returns:
            parsed_output: parsed output from pylint
        Raises:
            N/A
        """

        # Set up return objects
        parsed_output = {
            "score": 0,
            "metrics": {
                "errors": 0,
                "warnings": 0,
                "ignored": 0,
                "style_issues": 0,
                "design_issues": 0,
            },
            "errors": [],
            "warnings": [],
            "ignored": [],
            "style_issues": [],
            "design_issues": [],
            "summary": "",
        }

        # Set up Regex for parsing
        error_regex = r"^.*\.py\:\d+\: \[E"
        warning_regex = r"^.*\.py\:\d+\: \[W"
        ignored_regex = r"^.*\.py\:\d+\: \[I"
        style_regex = r"^.*\.py\:\d+\: \[C"
        design_regex = r"^.*\.py\:\d+\: \[R"
        summary_regex = r"^Your code has been rated at"

        for output_line in raw_pylint_stdout:

            # Getting the Message Type
            message_type = None
            if re.match(error_regex, output_line):
                message_type = "errors"
            elif re.match(warning_regex, output_line):
                message_type = "warnings"
            elif re.match(ignored_regex, output_line):
                message_type = "ignored"
            elif re.match(style_regex, output_line):
                message_type = "style_issues"
            elif re.match(design_regex, output_line):
                message_type = "design_issues"
            elif re.match(summary_regex, output_line):
                message_type = "summary"

            # Updating Report
            if not message_type:
                # non-matching line
                continue
            elif message_type in (
                "errors",
                "warnings",
                "ignored",
                "style_issues",
                "design_issues",
            ):
                # If error detail, append to data
                parsed_output["metrics"][message_type] += 1
                parsed_output[message_type].append(output_line)
            elif message_type == "summary":
                # Else, update summary data
                parsed_output["summary"] = output_line
                parsed_output["score"] = re.findall(
                    r"-{0,1}\d{1,2}\.\d{2}\/10", parsed_output["summary"]
                )[0].split("/")[0]
            else:
                # non-matching line
                continue

        # Set Total for Reporting
        parsed_output["metrics"]["total"] = sum(parsed_output["metrics"].values())

        # Stringify Errors/Warning/Notes for Reporting
        for message_type in (
            "errors",
            "warnings",
            "ignored",
            "style_issues",
            "design_issues",
        ):
            parsed_output[f"{message_type}_str"] = "\n".join(
                parsed_output[message_type]
            )
            if not parsed_output[f"{message_type}_str"]:
                parsed_output[f"{message_type}_str"] = "N/A"

        return parsed_output
