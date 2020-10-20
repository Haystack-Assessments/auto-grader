"""
Purpose:
    Module for running subprocess calls
"""

# Python Library Imports
import os
import pexpect
import subprocess
from typing import Any, Dict, List, Tuple

# Local Python Library Imports
# N/A


###
# Functions
###


def run_subprocess_call(
    command: str, env: Dict[str, Any], cwd: os.getcwd(), timeout: int = 60
) -> Tuple[List[str], List[str]]:

    """
    Purpose:
        Run a subprocess call. Check for normal errors, parse stdout and stderr
    Args:
        command: command to run
        env: environment variables for shell
        cwd: working directory to run command from
        timeout: timeout for command to complete
    Return:
        process_stdout: list of output split by newline
        process_stderr: list of output split by newline
    Raises:
        pexpect.exceptions.TIMEOUT: if command times out
    """

    child_process = subprocess.Popen(
        command,
        cwd=cwd,
        env=env,
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    # child_process.wait() did not return for large datasets (pylinting flask)
    while child_process.poll() is not None:
        continue

    child_process_stdout = [
        output_line
        for output_line in child_process.stdout.read().decode("utf-8").split("\n")
    ]
    child_process_stderr = [
        output_line
        for output_line in child_process.stderr.read().decode("utf-8").split("\n")
    ]

    return (child_process_stdout, child_process_stderr)
