"""
Purpose:
    Flake8 Class Definition

    Responsible for interacting with Flake8
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


class Flake8(Tool):
    """
    Purpose:
        Responsible for interacting with Flake8
    """

    default_args = [("--max-complexity", 10), ("--max-line-length", 88)]
    default_flags = ["--statistics"]

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
            source_code,
            python_package=python_package,
            args=args,
            flags=flags,
        )

    def __repr__(self) -> str:
        """
        Purpose:
            String Representation for a Flake8
        Args:
            N/A
        Returns:
            flake8_repr: command that will be run
        Raises:
            N/A
        """

        return f"<Flake8 {self.command})>"

    ###
    # Properties
    ###

    @property
    def command(self):
        """
        Purpose:
            Get the Flake8 command
        Args:
            N/A
        Returns:
            N/A
        Raises:
            N/A
        """

        parsed_args = " ".join([f"{arg}={value}" for (arg, value) in self.args])
        parsed_flags = " ".join(self.flags)

        return f"python3 -m flake8 {parsed_flags} {parsed_args} {self.python_package}"

    ###
    # Flake8 Operations
    ###

    def run(self) -> Dict[str, Any]:
        """
        Purpose:
            Run Flake8 tool against the target code
        Args:
            N/A
        Returns:
            flake8_stdout: parsed output from flake8
        Raises:
            N/A
        """

        # Run Flake8 command with pexpect and capture output
        (raw_flake8_stdout, _) = subprocess.run_subprocess_call(
            command=self.command, env={}, cwd=self.source_code, timeout=60
        )

        return self._parse_output(raw_flake8_stdout)

    def _parse_output(self, raw_flake8_stdout: bytes) -> Dict[str, Any]:
        """
        Purpose:
            Parse the Flake8 output to get standarized results for reporting
        Args:
            raw_flake8_stdout: raw output from the flake8 command
        Returns:
            N/A
        Raises:
            N/A
        """

        # Set up return objects
        parsed_output = {
            "metrics": {
                "errors": 0,
                "warnings": 0,
                "namings": 0,
                "flakes": 0,
                "complexities": 0,
            },
            "errors": [],
            "warnings": [],
            "namings": [],
            "flakes": [],
            "complexities": [],
            "summary": [],
        }

        # Set up Regex for parsing
        error_regex = r"^.*\.py\:\d+\:\d+\: E"
        warning_regex = r"^.*\.py\:\d+\:\d+\: W"
        naming_regex = r"^.*\.py\:\d+\:\d+\: N"
        flake_regex = r"^.*\.py\:\d+\:\d+\: F"
        complexity_regex = r"^.*\.py\:\d+\:\d+\: C"
        summary_regex = r"^[0-9]"

        for output_line in raw_flake8_stdout:

            # Getting the Message Type
            message_type = None
            if re.match(error_regex, output_line):
                message_type = "errors"
            elif re.match(warning_regex, output_line):
                message_type = "warnings"
            elif re.match(naming_regex, output_line):
                message_type = "namings"
            elif re.match(flake_regex, output_line):
                message_type = "flakes"
            elif re.match(complexity_regex, output_line):
                message_type = "complexities"
            elif re.match(summary_regex, output_line):
                message_type = "summary"

            # Updating Report
            if not message_type:
                # non-matching line
                continue
            elif message_type in (
                "errors",
                "warnings",
                "namings",
                "flakes",
                "complexities",
            ):
                # If error detail, append to data
                parsed_output["metrics"][message_type] += 1
            else:
                # non-matching line
                continue

            parsed_output[message_type].append(output_line)

        # Set Total for Reporting
        parsed_output["metrics"]["total"] = sum(parsed_output["metrics"].values())

        # Stringify Errors/Warning/Notes for Reporting
        for message_type in (
            "errors",
            "warnings",
            "namings",
            "flakes",
            "complexities",
            "summary",
        ):
            parsed_output[f"{message_type}_str"] = "\n".join(
                parsed_output[message_type]
            )
            if not parsed_output[f"{message_type}_str"]:
                parsed_output[f"{message_type}_str"] = "N/A"

        return parsed_output
