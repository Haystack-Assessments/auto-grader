"""
Purpose:
    Holds python object of the report ranking template. Allows for string replacement
    .md and .html generation
"""


###
# HTML Definition
###


report_ranking_html_template = """
<!DOCTYPE html>
<html>
<body>

<style>
</style>

<h1>Ranking Report</h1>

<p>The following report ranks candidates that have already been assessed</p>

<div id="table_of_contents">
<h2 class="table_of_contents_title">Table of Contents</h2>
<ul class="table_of_contents_contents">
    <li><a href="#Candidates">Candidates</a></li>
    <li><a href="#Code_Errors">Code Errors</a></li>
    <li><a href="#Pylint_Scores">Pylint Scores</a></li>
    <li><a href="#Test_Breakdown">Test Breakdown</a></li>
</ul>
</div>

<h2 id="Candidates">Candidates</h2>

<p>
{candidate_list_html}
</p>

<h2 id="Code_Errors">Code Errors</h2>

<p>
Summary of Error Counts By Candidate and Tool:
</p>

<img src="assets/error_count_line_chart.png" alt="Error Count">

<h2 id="Pylint_Scores">Pylint Scores</h2>

<p>
Test Success/Fail Percentage Breakdown By Candidate:
</p>

<img src="assets/pylint_scores_by_candidate.png" alt="Pylint Scores">

<h2 id="Test_Breakdown">Test Breakdown</h2>

<p>
Test Success/Fail Percentage Breakdown By Candidate:
</p>

<img src="assets/test_breakdown_pie_charts.png" alt="Test Success">

</body>
</html>
"""
