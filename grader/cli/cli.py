#!/usr/bin/env python3
"""
Purpose:
    Entrypoint for running the Python Grader Tool
"""

# Python Library Imports
import click

# Local Python Library Imports
import grader.commands.report_commands as report_commands


###
# CLI Entrypoint
###


@click.group(invoke_without_command=True)
@click.version_option("0.0.1")
@click.pass_context
def pygrader_cli(cli_context):
    """
    PyGrader CLI
    """

    pass


###
# Command Groups
###


@pygrader_cli.group("report")
@click.pass_context
def report_command_group(cli_context):
    """
    Report Command Group interacts and creates PyGrade Reports
    """

    pass


###
# CLI Setup
###


def setup_grader_cli() -> None:
    """
    Purpose:
        Setup the python grader CLI
    Args:
        N/A
    Returns:
        N/A
    Raises:
        N/A
    """

    report_command_group.add_command(report_commands.generate)
