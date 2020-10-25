"""
Purpose:
    Holds python object of the python report template. Allows for string replacement
    .md and .html generation
"""


###
# HTML Definition
###


report_python_html_template = """
<!DOCTYPE html>
<html>
<body>

<style>
pre {{
    white-space: pre-wrap;
    background: #f1f1f1;
}}
</style>

<h1>Code Quality Report</h1>

<p>The following report details the overall quality of the repo</p>

<div id="table_of_contents">
<h2 class="table_of_contents_title">Table of Contents</h2>
<ul class="table_of_contents_contents">
    <li><a href="#Candidate">Candidate</a></li>
    <li><a href="#Code_Summary">Code_Summary</a></li>
    <li><a href="#Performance_Profiling">Performance_Profiling</a></li>
    <ul class="table_of_contents_contents_performance">
        <li><a href="#Execution_Time">Execution Time</a></li>
        <li><a href="#Memory_Usage">Memory Usage</a></li>
    </ul>
    <li><a href="#Tests">Tests</a></li>
    <ul class="table_of_contents_contents_tests">
        <li><a href="#Tests_Summary">Summary</a></li>
        <li><a href="#Tests_Details">Details</a></li>
    </ul>
    <li><a href="#Coverage">Coverage</a></li>
    <ul class="table_of_contents_contents_coverage">
        <li><a href="#Coverage_Summary">Summary</a></li>
        <li><a href="#Coverage_Details">Details</a></li>
    </ul>
    <li><a href="#Mypy">Mypy</a></li>
    <ul class="table_of_contents_contents_mypy">
        <li><a href="#Mypy_Summary">Summary</a></li>
        <li><a href="#Mypy_Details">Details</a></li>
    </ul>
    <li><a href="#Pylint">Pylint</a></li>
    <ul class="table_of_contents_contents_pylint">
        <li><a href="#Pylint_Summary">Summary</a></li>
        <li><a href="#Pylint_Details">Details</a></li>
    </ul>
    <li><a href="#Pycodestyle">Pycodestyle</a></li>
    <ul class="table_of_contents_contents_pycodestyle">
        <li><a href="#Pycodestyle_Summary">Summary</a></li>
        <li><a href="#Pycodestyle_Details">Details</a></li>
    </ul>
    <li><a href="#Flake8">Flake8</a></li>
    <ul class="table_of_contents_contents_flake8">
        <li><a href="#Flake8_Summary">Summary</a></li>
        <li><a href="#Flake8_Details">Details</a></li>
    </ul>
</ul>
</div>

<h2 id="Candidate">Candidate</h2>

<p>
<b>Candidate Name:</b> {candidate[name]}</br>
<b>Ranking:</b> <span style="color:black">TODO</span>
</p>

<h2 id="Code_Summary">Code Summary</h2>

<p>
TODO
</p>

<h2 id="Performance_Profiling">Performance Profiling</h2>

<p>
The following section details performance profiling of the solutions
</p>

<h3 id="Execution_Time">Execution Time</h2>

<p>
The following section details performance profiling of the solutions:
</p>

<pre>
TODO
</pre>

<h3 id="Memory_Usage">Memory Usage</h2>

<p>
The following shows the memory usage during the execution of the assessment code:
</p>

<pre>
TODO
</pre>

<h2 id="Tests">Tests</h2>

<p>
The following details results from python testing report:
</p>

<h3 id="Tests_Summary">Summary</h2>

<p>
The following section details performance profiling of the solutions:
</p>

<p>
<b>Total Tests</b>: {pytest[tests][metrics][total_tests]}
</p>

<p>
<b>Total Errors</b>: {pytest[tests][metrics][error_tests]}</br>
<b>Percentage Errors</b>: {pytest[tests][metrics][percentage_error]}%
</p>

<p>
<b>Total Failures</b>: {pytest[tests][metrics][failed_tests]}</br>
<b>Percentage Failing</b>: {pytest[tests][metrics][percentage_failed]}%
</p>

<p>
<b>Total Passes</b>: {pytest[tests][metrics][passed_tests]}</br>
<b>Percentage Passed</b>: {pytest[tests][metrics][percentage_passed]}%
</p>

<h3 id="Tests_Details">Details</h2>

<p>
The following shows the memory usage during the execution of the assessment code:
</p>

<b>Error Tests</b>:
<pre>
{pytest[tests][error_tests_str]}
</pre>

<b>Failed Tests</b>:
<pre>
{pytest[tests][failed_tests_str]}
</pre>

<b>Passed Test</b>:
<pre>
{pytest[tests][passed_tests_str]}
</pre>

<h2 id="Coverage">Coverage</h2>

The following details results from python coverage report:

<h3 id="Coverage_Summary">Summary</h2>

<p>
<b>Coverage Percentage</b>: {pytest[coverage][metrics][statements_percentage]}%
</p>

<p>
<b>Total Statements</b>: {pytest[coverage][metrics][statements_percentage]}</br>
<b>Missing Statements</b>: {pytest[coverage][metrics][statements_missing]}</br>
<b>Branching Statements</b>: {pytest[coverage][metrics][statements_branching]}
</p>

<h3 id="Coverage_Details">Details</h2>

<b>Coverage Per File</b>:
<pre>
{pytest[coverage][details_str]}
</pre>

<h2 id="Mypy">Mypy</h2>

The following details results from python static type checking:

<h3 id="Mypy_Summary">Summary</h2>

<p>
<b>Total Issues</b>: {mypy[metrics][total]}
</p>

<p>
<b>Errors</b>: {mypy[metrics][errors]}</br>
<b>Warnings</b>: {mypy[metrics][warnings]}</br>
<b>Notes</b>: {mypy[metrics][notes]}
</p>

<pre>
{mypy[summary]}
</pre>

<h3 id="Mypy_Details">Details</h2>

<b>Errors</b>:
<pre>
{mypy[errors_str]}
</pre>

<b>Warnings</b>:
<pre>
{mypy[warnings_str]}
</pre>

<b>Notes</b>:
<pre>
{mypy[notes_str]}
</pre>

<h2 id="Pylint">Pylint</h2>

The following details results from the Flake8 tool:

<h3 id="Pylint_Summary">Summary</h2>

<p>
<b>Total Issues</b>: {pylint[metrics][total]}</br>
<b>Overall Score</b>: {pylint[score]} / 10
</p>

<p>
<b>Errors</b>: {pylint[metrics][errors]}</br>
<b>Warnings</b>: {pylint[metrics][warnings]}</br>
<b>Ignored</b>: {pylint[metrics][ignored]}</br>
<b>Style Issues</b>: {pylint[metrics][style_issues]}</br>
<b>Design Issues</b>: {pylint[metrics][design_issues]}
</p>

<pre>
{pylint[summary]}
</pre>

<h3 id="Pylint_Details">Details</h2>

<b>Errors</b>:
<pre>
{pylint[errors_str]}
</pre>

<b>Warnings</b>:
<pre>
{pylint[warnings_str]}
</pre>

<b>Ignored Items</b>:
<pre>
{pylint[ignored_str]}
</pre>

<b>Style Issues</b>:
<pre>
{pylint[style_issues_str]}
</pre>

<b>Design Issues</b>:
<pre>
{pylint[design_issues_str]}
</pre>

<h2 id="Pycodestyle">Pycodestyle</h2>

The following details results from the Flake8 tool:

<h3 id="Pycodestyle_Summary">Summary</h2>

<p>
<b>Total Issues</b>: {pycodestyle[metrics][total]}
</p>

<p>
<b>Errors</b>: {pycodestyle[metrics][errors]}</br>
<b>Warnings</b>: {pycodestyle[metrics][warnings]}
</p>

<pre>
{pycodestyle[summary_str]}
</pre>

<h3 id="Pycodestyle_Details">Details</h2>

<b>Errors</b>:
<pre>
{pycodestyle[errors_str]}
</pre>

<b>Warnings</b>:
<pre>
{pycodestyle[warnings_str]}
</pre>

<h2 id="Flake8">Flake8</h2>

The following details results from the Flake8 tool:

<h3 id="Flake8_Summary">Summary</h2>

<p>
<b>Total Issues</b>: {flake8[metrics][total]}
</p>

<p>
<b>Errors</b>: {flake8[metrics][errors]}</br>
<b>Warnings</b>: {flake8[metrics][warnings]}</br>
<b>Naming</b>: {flake8[metrics][namings]}</br>
<b>Design (Flakes)</b>: {flake8[metrics][flakes]}</br>
<b>Complexity (Mccabe)</b>: {flake8[metrics][complexities]}
</p>

<pre>
{flake8[summary_str]}
</pre>

<h3 id="Flake8_Details">Details</h2>

<b>Errors</b>:
<pre>
{flake8[errors_str]}
</pre>

<b>Warnings</b>:
<pre>
{flake8[warnings_str]}
</pre>

<b>Naming Issues</b>:
<pre>
{flake8[namings_str]}
</pre>

<b>Complexity Issues</b>:
<pre>
{flake8[complexities_str]}
</pre>

<b>Design Issues</b>:
<pre>
{flake8[flakes_str]}
</pre>


</body>
</html>
"""

###
# Markdown Definition
###


report_python_md_template = """
# Code Quality Report

The following report details the overall quality of the repo

## Table of Contents

* [Candidate](#candidate)
* [Code Summary](#code-summary)
* [Performance Profiling](#performance-profiling)
* [Tests](#tests)
* [Coverage](#coverage)
* [Mypy](#mypy)
* [Pylint](#pylint)
* [Pycodestyle](#pycodestyle)
* [Flake8](#flake8)

## Candidate

**Name**: {candidate[name]}

## Candidate Review

Manual Overview

## Code Summary

Manual Summary

## Performance Profiling

The following section details performance profiling of the solutions

### Execution Time

The following shows the execution time of the solution using different inputs

```bash
TODO
```

### Memory Usage

The following shows the memory usage during the execution of the assessment code

```bash
TODO
```

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
