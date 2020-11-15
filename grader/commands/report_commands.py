"""
    Purpose:
        Report Command Group is responsible for generating reports
"""

# Python Library Imports
import click

# Local Python Library Imports
from grader.report.report_python import ReportPython
from grader.report.report_ranking import ReportRanking


###
# Report Commands
###


@click.command("generate")
@click.option(
    "--source",
    "source_code",
    required=True,
    default=None,
    type=str,
    help="Source Code to Grade",
)
@click.option(
    "--package",
    "python_package",
    required=False,
    default="assessment_python_proficiency",
    type=str,
    help="Package to Grade",
)
@click.option(
    "--report",
    "report_name",
    required=True,
    default=None,
    type=str,
    help="Name of the Report",
)
@click.option(
    "--candidate",
    "candidate_name",
    required=True,
    default=None,
    type=str,
    help="Name of the Candidate",
)
@click.option(
    "--overwrite",
    flag_value=True,
    type=bool,
    default=False,
    help="Overwrite report if it already exists?",
)
@click.pass_context
def generate(
    cli_context: object,
    report_name: str,
    candidate_name: str,
    source_code: str,
    python_package: str,
    overwrite: bool,
) -> None:
    """
    Generate a pygrade report
    """
    click.echo("Generating Candidate Report")

    # Build base report object
    pygrade_report = ReportPython(
        report_name, candidate_name, source_code, python_package
    )

    # Generate the report
    pygrade_report.generate_report(overwrite=overwrite)

    click.echo(f"Report Created: {pygrade_report.report_path}")


@click.command("rank")
@click.option(
    "--report",
    "report_name",
    required=True,
    default=None,
    type=str,
    help="Name of the Report",
)
@click.option(
    "--candidates",
    "candidate_path",
    required=False,
    default=None,
    type=str,
    help="Where are Candidate Reports to Rank",
)
@click.option(
    "--overwrite",
    flag_value=True,
    type=bool,
    default=False,
    help="Overwrite report if it already exists?",
)
@click.pass_context
def rank(
    cli_context: object,
    report_name: str,
    candidate_path: str,
    overwrite: bool,
) -> None:
    """
    Generate a pygrade report
    """
    click.echo("Generating Ranking Report")

    # Build base report object
    ranking_report = ReportRanking(report_name, candidate_path)

    # Generate the report
    ranking_report.generate_report(overwrite=overwrite)

    click.echo(f"Report Created: {ranking_report.report_path}")
