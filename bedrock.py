import sys
import json
import boto3

client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

print("analyzing the report")

model_id = "us.anthropic.claude-sonnet-4-6"

file_path = sys.argv[1]

with open(file_path, "r") as f:
    report_json = json.load(f)

report_data = json.dumps(report_json)

prompt = f"""
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

print(model_response["content"][0]["text"])