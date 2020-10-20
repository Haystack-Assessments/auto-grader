# Haystack Assessments: auto-grader

Repository for Automatic Grading/Assessment of Code.

The auto-grader tool is being built as a tool for running automation against multiple programming languages to create an overall health of the repository.

## Table of Contents

- [Dependencies](#dependencies)
- [How To](#how-to)
- [Notes](#notes)
- [TODO](#todo)

## Dependencies/System Requirements

Dependencies for auto-grader

### Python Packages

* python>=3.6

## How-To

### Install

auto-grader is a python package to be installed with pip.

```bash
localhost$ pip3 install auto-grader
```

### Generate Report

```bash
localhost$ grader_python report generate --report={NAME} --source={PATH_TO_CODE} --candidate={CANDIDATE_NAME}
```

## Notes

* Current implementation is a proof of concept and not fully implemented for all use-cases

## TODO

* TBD
