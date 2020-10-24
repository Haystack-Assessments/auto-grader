#!/usr/bin/env python3
"""
    Purpose:
        Used for packaging, testing, and building the project
"""

# Python Imports
import os
import re
from setuptools import setup, find_packages
from typing import List


###
# Helper Functions
###


def get_version_from_file(python_version_file: str) -> str:
    """
    Purpose:
        Get python version from a specified requirements file.
    Args:
        python_version_file: Path to the version file
    Return:
        requirements: string representation of the version
    Raises:
        N/A
    """

    version = "development"
    if os.path.isfile(python_version_file):
        with open(python_version_file) as version_file:
            version = version_file.readline().strip().strip("\n")

    return version


def get_requirements_from_file(python_requirements_file: str) -> List[str]:
    """
    Purpose:
        Get python requirements from a specified requirements file.
    Args:
        python_requirements_file: Path to the requirements file
    Return:
        requirements: List of requirements
    """

    requirements = []
    if os.path.isfile(python_requirements_file):
        with open(python_requirements_file) as requirements_file:
            requirement = requirements_file.readline()
            while requirement:
                if requirement.strip().startswith("#"):
                    pass
                elif requirement.strip() == "":
                    pass
                else:
                    requirements.append(requirement.strip())
                requirement = requirements_file.readline()

    return requirements


def get_readme(readme_file: str) -> str:
    """
    Purpose:
        Return the README details from the README.md for documentation
    Args:
        readme_file: Project README file
    Return:
        requirement_files: README file data
    """

    readme_data = "Description Not Found"
    if os.path.isfile(readme_file):
        with open(readme_file, "r") as readme_file_object:
            readme_data = readme_file_object.read()

    return readme_data


###
# Main Functionality
###


def main() -> None:
    """
    Purpose:
        Main function for packaging and setting up packages
    Args:
        N/A
    Return:
        N/A
    """

    # Get Version and README
    version = get_version_from_file("./VERSION")
    readme = get_readme("./README.md")

    # Get Packages
    packages = find_packages()

    # Get Requirements
    install_requirements = []
    test_requirements = []
    for package in packages:
        install_requirements.extend(
            get_requirements_from_file(f"{package}/requirements.txt")
        )
        test_requirements.extend(
            get_requirements_from_file(f"{package}/requirements_test.txt")
        )
    setup_requirements = [
        "pytest~=6.1.1",  # Execute Tests
        "pytest-cov~=2.10.1",  # Code Coverage
        "pytest-html~=2.1.1",  # Reports
        "pytest-runner==5.2",  # Runner
    ]

    # Get Dependency Links For Each Requirement (As Necessary)
    dependency_links = []

    setup(
        author="Haystack",
        author_email="Christopher.Hayden.Todd@gmail.com",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Framework :: Pytest",
        ],
        description=("Tool for grading software projects"),
        include_package_data=True,
        install_requires=install_requirements,
        keywords=["python"],
        long_description=readme,
        long_description_content_type="text/markdown",
        name="haystack-auto-grader",
        packages=packages,
        project_urls={},
        python_requires=">3.6",
        scripts=[
            "./grader/bin/grader_python",
            # TODO, other languages
        ],
        setup_requires=setup_requirements,
        tests_require=test_requirements,
        url="https://github.com/Haystack-Assessments/auto-grader",
        version=version,
    )


if __name__ == "__main__":
    main()
