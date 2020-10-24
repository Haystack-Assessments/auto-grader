"""
Purpose:
    Holds python object of the python report template. Allows for string replacement
    .md generation
"""

# Python Library Imports
# N/A

# Local Python Library Imports
# N/A


###
# Artifact Definition
###


report_python_template = """
# Code Quality Report

The following report details the overall quality of the repo

## Table of Contents

* [Candidate](#candidate)
* [Code Summary](#code-summary)
* [Tests](#tests)
* [Coverage](#coverage)
* [Mypy](#mypy)
* [Pylint](#pylint)
* [Pycodestyle](#pycodestyle)
* [Flake8](#flake8)

## Candidate

**Name**: {candidate[name]}

## Candidate Review

Manual Review TODO

## Code Summary

TODO Automation

## Tests

The following details results from python testing report:

### Summary

**Total Tests**: {pytest[tests][metrics][total_tests]}

**Total Errors**: {pytest[tests][metrics][error_tests]}
**Percentage Errors**: {pytest[tests][metrics][percentage_error]}%

**Total Failures**: {pytest[tests][metrics][failed_tests]}
**Percentage Failing**: {pytest[tests][metrics][percentage_failed]}%

**Total Passes**: {pytest[tests][metrics][passed_tests]}
**Percentage Passed**: {pytest[tests][metrics][percentage_passed]}%

### Details

**Error Tests**:
```bash
{pytest[tests][error_tests_str]}
```

**Failed Tests**:
```bash
{pytest[tests][failed_tests_str]}
```

**Passed Test**:
```bash
{pytest[tests][passed_tests_str]}
```

## Coverage

The following details results from python coverage report:

### Summary

**Coverage Percentage**: {pytest[coverage][metrics][statements_percentage]}%

**Total Statements**: {pytest[coverage][metrics][statements_percentage]}
**Missing Statements**: {pytest[coverage][metrics][statements_missing]}
**Branching Statements**: {pytest[coverage][metrics][statements_branching]}

### Details

**Coverage Per File**:
```bash
{pytest[coverage][details_str]}
```

## Mypy

The following details results from python static type checking:

### Summary

**Total Issues**: {mypy[metrics][total]}

**Errors**: {mypy[metrics][errors]}
**Warnings**: {mypy[metrics][warnings]}
**Notes**: {mypy[metrics][notes]}

```bash
{mypy[summary]}
```

### Details

**Errors**:
```bash
{mypy[errors_str]}
```

**Warnings**:
```bash
{mypy[warnings_str]}
```

**Notes**:
```bash
{mypy[notes_str]}
```

## Pylint

The following details results from the Flake8 tool:

### Summary

**Total Issues**: {pylint[metrics][total]}
**Overall Score**: {pylint[score]} / 10

**Errors**: {pylint[metrics][errors]}
**Warnings**: {pylint[metrics][warnings]}
**Ignored**: {pylint[metrics][ignored]}
**Style Issues**: {pylint[metrics][style_issues]}
**Design Issues**: {pylint[metrics][design_issues]}

```bash
{pylint[summary]}
```

### Details

**Errors**:
```bash
{pylint[errors_str]}
```

**Warnings**:
```bash
{pylint[warnings_str]}
```

**Ignored Items**:
```bash
{pylint[ignored_str]}
```

**Style Issues**:
```bash
{pylint[style_issues_str]}
```

**Design Issues**:
```bash
{pylint[design_issues_str]}
```

## Pycodestyle

The following details results from the Flake8 tool:

### Summary

**Total Issues**: {pycodestyle[metrics][total]}

**Errors**: {pycodestyle[metrics][errors]}
**Warnings**: {pycodestyle[metrics][warnings]}

```bash
{pycodestyle[summary_str]}
```

### Details

**Errors**:
```bash
{pycodestyle[errors_str]}
```

**Warnings**:
```bash
{pycodestyle[warnings_str]}
```

## Flake8

The following details results from the Flake8 tool:

### Summary

**Total Issues**: {flake8[metrics][total]}

**Errors**: {flake8[metrics][errors]}
**Warnings**: {flake8[metrics][warnings]}
**Naming**: {flake8[metrics][namings]}
**Design (Flakes)**: {flake8[metrics][flakes]}
**Complexity (Mccabe)**: {flake8[metrics][complexities]}

```bash
{flake8[summary_str]}
```

### Details

**Errors**:
```bash
{flake8[errors_str]}
```

**Warnings**:
```bash
{flake8[warnings_str]}
```

**Naming Issues**:
```bash
{flake8[namings_str]}
```

**Complexity Issues**:
```bash
{flake8[complexities_str]}
```

**Design Issues**:
```bash
{flake8[flakes_str]}
```
"""

# candidate_report_template = """
# # Code Quality Report

# The following report details the overall quality of the repo

# ## Table of Contents

# * [Candidate](#candidate)
# * [Summary](#summary)
# * [Tests](#tests)
# * [Coverage](#coverage)
# * [Typing](#typing)
# * [Style](#style)
#     * [Pylint](#pylint)
#     * [Pycodestyle](#pycodestyle)
#     * [Flake8](#flake8)

# ## Candidate

# **Name**: {candidate.name}
# **Email**: {candidate.email}

# ## Overview

# Below is an overview of results

# ### Summary

# The candidate created a

# ### Design

# The solution ...

# ## Tests

# The following details results of automated testing using Pytest:

# ### Summary

# **Total Tests**: {TODO}
# **Total Passed**: {TODO}
# **Total Failed**: {TODO}
# **Percentage Passed**: {TODO}

# ### Details

# ```bash
# {TODO}
# ```

# ### Report

# Report is located ...

# ## Coverage

# The following details results of automated testing using Pytest-cov:

# ### Summary

# **Code Coverage**: {TODO}

# ### Details

# ```bash
# TBD
# ```

# ### Report

# Report is located ...

# ## Typing

# The following details results from python static type checking:

# ### Summary

# **Errors**: {TODO}
# **Warning**: {TODO}

# ### Details

# ```bash
# {TODO}
# ```

# ## Style

# The following detail results from various python style tools:

# ### Pylint

# The following details results from the Pylint tool:

# #### Summary

# **Score**: {TODO}/10
# **Fatal**: {TODO}
# **Error**: {TODO}
# **Warning**: {TODO}
# **Convention**: {TODO}
# **Refactor**: {TODO}

# #### Details

# ```bash
# {TODO}
# ```

# ### Pycodestyle

# The following details results from the Pycodestyle tool:

# #### Summary

# **Errors**: {TODO}
# **Warnings**: {TODO}

# ```bash
# {TODO}
# ```

# #### Details

# ```bash
# {TODO}
# ```

# ### Flake8

# The following details results from the Flake8 tool:

# #### Summary

# **Errors**: {TODO}
# **Warnings**: {TODO}
# **Naming**: {TODO}
# **Design (Flakes)**: {TODO}
# **Complexity (Mccabe)**: {TODO}

# ```bash
# {TODO}
# ```

# #### Details

# ```bash
# {TODO}
# ```
# """
