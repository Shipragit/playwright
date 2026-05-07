import sys
import os
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Read report file path from command line
file_path = sys.argv[1]

# Open and read JSON report
with open(file_path, "r") as f:
    report_json = json.load(f)

# Convert full report to string for AI
report_data = json.dumps(report_json)

# Counters
passed = 0
failed = 0

# Parse Playwright JSON report
for suite in report_json.get("suites", []):
    for spec in suite.get("specs", []):
        for test in spec.get("tests", []):
            for result in test.get("results", []):
                status = result.get("status")

                if status == "passed":
                    passed += 1

                elif status == "failed":
                    failed += 1

print("🔍 Playwright Report Analysis Started...\n")

# If all tests passed
if failed == 0:
    print("✅ AI Analysis Completed")
    print(f"✔ Total Passed Tests : {passed}")
    print(f"❌ Total Failed Tests : {failed}")
    print("\n🎉 No test cases failed. You are good!")
    sys.exit(0)

# If failures exist
print(f"✔ Total Passed Tests : {passed}")
print(f"❌ Total Failed Tests : {failed}")

print("\n🧠 Sending failed test details to OpenAI...\n")

# Send failure data to OpenAI
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a QA automation expert. "
                "Analyze Playwright test failures and provide root cause analysis."
            )
        },
        {
            "role": "user",
            "content": f"""
Analyze this Playwright test report.

Provide:
1. Why the tests failed
2. Root cause analysis
3. Suggested fixes
4. Important observations

Playwright Report:
{report_data[:12000]}
"""
        }
    ]
)

# Print AI response
print("\n🧠 AI Failure Analysis Result:\n")
print(response.choices[0].message.content)