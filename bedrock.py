import sys
import json
import boto3

client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

print("Analyzing the Test report by aws bedrock (claude-sonnet-4-6")

model_id = "us.anthropic.claude-sonnet-4-6"

file_path = sys.argv[1]

with open(file_path, "r") as f:
    report_json = json.load(f)

report_data = json.dumps(report_json)

prompt = f"""
Think like you are QA expert,
Analyze this Playwright test report.

Provide:
1. Failed test summary
2. Root cause
3. Suggested fix

Report:
{report_data[:12000]}
"""

native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 512,
    "temperature": 0.5,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
}

response = client.invoke_model(
    modelId=model_id,
    body=json.dumps(native_request)
)

model_response = json.loads(response["body"].read())

ai_result = model_response["content"][0]["text"]

print(ai_result)

with open("ai-analysis.txt", "w") as f:
    f.write(ai_result)

print("\nAI analysis saved into ai-analysis.txt")