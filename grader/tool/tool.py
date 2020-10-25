"""
Purpose:
    Tool Class Definition

    Abstract Base Class for Tools
"""

# Python Library Imports
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

# Local Python Library Imports
# N/A


###
# Class Definition
###


class Tool:
    """
    Purpose:
        Abstract Base Class for Tools
    """

    default_args = []
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
            Constructor for a Pylint
        Args:
            source_code: code to run pylint on
            python_package: python_package to assess
            args: argument overrides for pylint
            flags: flag overrides for pylint
        Returns:
            N/A
        Raises:
            Exception: If the path to code is not valid
        """

        # Code Data
        self.args = args or self.default_args
        self.flags = flags or self.default_flags
        self.source_code = source_code
        if python_package:
            self.code_dir = f"{source_code}/{python_package}"
            self.python_package = python_package
        else:
            self.code_dir = source_code
            self.python_package = "*"

        # Validate Code Dir Exists
        if not os.path.isdir(source_code):
            raise Exception(f"{source_code} is not a valid path to code")

    ###
    # Properties
    ###

    @property
    @abstractmethod
    def command(self):
        """
        Purpose:
            The command to run the tool
        Args:
            N/A
        Returns:
            N/A
        Raises:
            N/A
        """

        pass

    ###
    # Tool Operations
    ###

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Purpose:
            Run tool against the target code
        Args:
            N/A
        Returns:
            parsed_tool_output: parsed output from the tool
        Raises:
            N/A
        """

        pass
