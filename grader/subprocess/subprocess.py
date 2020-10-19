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


# def run_subprocess_call(
#     command: str,
#     env: Dict[str, Any],
#     cwd: os.getcwd(),
#     timeout: int = 60,
# ) -> List[str]:

#     """
#     Purpose:
#         Run a subprocess call. Check for normal errors, parse stdout and stderr
#     Args:
#         command: command to run
#         env: environment variables for shell
#         cwd: working directory to run command from
#         timeout: timeout for command to complete
#     Return:
#         process_output: list of output split by newline
#     Raises:
#         pexpect.exceptions.TIMEOUT
#     """

#     child_process = pexpect.spawn(command, env=env, timeout=timeout, cwd=cwd)

#     try:
#         expect_idx = child_process.expect([pexpect.EOF], timeout=timeout)
#     except pexpect.exceptions.TIMEOUT:
#         print(f"Subprocess Call Failed: {command}")
#         raise

#     child_process.close()
#     # if child_process.exitstatus != 0:
#     #     raise Exception(f"Command failed with exitstatus {child_process.exitstatus}: {command}")

#     return [output_line for output_line in child_process.before.decode("utf-8").split("\r\n")]
