"""
Purpose:
    Mypy Class Definition

    Responsible for interacting with Mypy
"""

# Python Library Imports
import os
import re
from typing import Any, Dict, List, Optional

# Local Python Library Imports
import grader.subprocess.subprocess as subprocess


###
# Class Definition
###


class Mypy:
    """
    Purpose:
        Responsible for interacting with Mypy
    """

    default_args = ()
    default_flags = [
        "--allow-untyped-defs",
        "--disallow-untyped-calls",
        "--disallow-incomplete-defs",
        "--ignore-missing-imports",
        "--namespace-packages",
        "--no-color-output",
    ]

    ###
    # Reserved Methods
    ###

    def __init__(
        self,
        source_code: str,
        args: Optional[Dict[str, str]] = None,
        flags: Optional[List[str]] = None,
    ) -> None:
        """
        Purpose:
            Constructor for a Mypy
        Args:
            source_code: code to run mypy on
            args: argument overrides for mypy
            flags: flag overrides for mypy
        Returns:
            N/A
        Raises:
            Exception: If the path to code is not valid
        """

        if not os.path.isdir(source_code):
            raise Exception(f"{source_code} is not a valid path to code")

        self.source_code = source_code
        self.args = args or self.default_args
        self.flags = flags or self.default_flags

    def __repr__(self) -> str:
        """
        Purpose:
            String Representation for a Mypy
        Args:
            N/A
        Returns:
            mypy_repr: command that will be run
        Raises:
            N/A
        """

        return f"<Mypy {self.command})>"

    ###
    # Properties
    ###

    @property
    def command(self):
        """
        Purpose:
            Get the Mypy command
        Args:
            N/A
        Returns:
            N/A
        Raises:
            N/A
        """

        parsed_args = " ".join([f"{arg}={value}" for (arg, value) in self.args])
        parsed_flags = " ".join(self.flags)

        return f"python3 -m mypy {parsed_flags} {parsed_args}"

    ###
    # Mypy Operations
    ###

    def run(self) -> Dict[str, Any]:
        """
        Purpose:
            Run Mypy tool against the target code
        Args:
            N/A
        Returns:
            mypy_stdout: parsed output from mypy
        Raises:
            N/A
        """

        # Run Mypy command with pexpect and capture output
        (raw_mypy_stdout, _) = subprocess.run_subprocess_call(
            command=self.command, env={}, cwd=self.source_code, timeout=60
        )

        return self._parse_output(raw_mypy_stdout)

    def _parse_output(self, raw_mypy_stdout: bytes) -> Dict[str, Any]:
        """
        Purpose:
            Parse the Mypy output to get standarized results for reporting
        Args:
            raw_mypy_stdout: raw output from the mypy command
        Returns:
            N/A
        Raises:
            N/A
        """

        # Set up return objects
        parsed_output = {
            "metrics": {"warnings": 0, "notes": 0, "errors": 0},
            "errors": [],
            "warnings": [],
            "notes": [],
            "summary": "",
        }

        # Set up Regex for parsing
        error_regex = r"^.*\.py\:\d+\: error\:"
        note_regex = r"^.*\.py\:\d+\: note\:"
        warning_regex = r"^.*\.py\:\d+\: warning\:"
        found_errors_regex = r"^Found \d+ errors"
        no_errors_regex = r"^Success: no issues"

        for output_line in raw_mypy_stdout:

            # Getting the Message Type
            message_type = None
            if re.match(error_regex, output_line):
                message_type = "errors"
            elif re.match(warning_regex, output_line):
                message_type = "warnings"
            elif re.match(note_regex, output_line):
                message_type = "notes"
            elif re.match(found_errors_regex, output_line) or re.match(
                no_errors_regex, output_line
            ):
                message_type = "summary"

            # Updating Report
            if not message_type:
                # non-matching line
                continue
            if message_type in ("errors", "warnings", "notes"):
                # If error detail, append to data
                parsed_output["metrics"][message_type] += 1
                parsed_output[message_type].append(output_line)
            elif message_type == "summary":
                # Else, update summary data
                parsed_output["summary"] = output_line
            else:
                # non-matching line
                continue

        # Set Total for Reporting
        parsed_output["metrics"]["total"] = sum(parsed_output["metrics"].values())

        # Stringify Errors/Warning/Notes for Reporting
        for message_type in ("errors", "warnings", "notes"):
            parsed_output[f"{message_type}_str"] = "\n".join(
                parsed_output[message_type]
            )

        return parsed_output
