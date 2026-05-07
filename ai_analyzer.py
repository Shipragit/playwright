import sys
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Read report file path from command line
file_path = sys.argv[1]

# Open and read report file
with open(file_path, "r") as f:
    report_data = f.read()

print("🔍 Sending Playwright report to AI for analysis...")

# Send report to OpenAI
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a QA automation expert. "
                "Analyze Playwright test failures and provide useful debugging insights."
            )
        },
        {
            "role": "user",
            "content": f"""
Analyze this Playwright test report and provide:

1. Failed test summary
2. Possible root causes
3. Suggested fixes
4. Important observations

Playwright Report:
{report_data[:12000]}
"""
        }
    ]
)

# Print AI response
print("\n🧠 AI Analysis Result:\n")
print(response.choices[0].message.content)