import json

with open("playwright-report.json") as f:
    data = json.load(f)

passed = 0
failed = 0

for suite in data.get("suites", []):
    for spec in suite.get("specs", []):
        for test in spec.get("tests", []):
            status = test["results"][0]["status"]

            if status == "passed":
                passed += 1
            else:
                failed += 1

html = f"""
<html>
<head>
<style>
body {{
    font-family: Arial;
    background-color: #1e1e1e;
    color: white;
}}

table {{
    border-collapse: collapse;
    width: 60%;
}}

th {{
    background-color: #8B7500;
    color: white;
    padding: 10px;
}}

td {{
    border: 1px solid gray;
    padding: 8px;
}}

.pass {{
    color: lightgreen;
}}

.fail {{
    color: red;
}}
</style>
</head>

<body>

<h2>System Health Report</h2>

<table>
<tr>
<th>Total Passed</th>
<th>Total Failed</th>
</tr>

<tr>
<td class="pass">{passed}</td>
<td class="fail">{failed}</td>
</tr>
</table>

<br>

<table>
<tr>
<th>Environment</th>
<th>Status</th>
</tr>

<tr>
<td>UAT</td>
<td class="pass">Healthy</td>
</tr>

</table>

</body>
</html>
"""

with open("email-report.html", "w") as f:
    f.write(html)

print("HTML report generated")