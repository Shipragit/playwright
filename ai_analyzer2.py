from openai import OpenAI
import os

print("Starting AI Analyzer...")

# Read API key from GitHub Secret / Environment Variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY not found")
    exit(1)

# Create OpenAI client
client = OpenAI(api_key=api_key)

try:
    # Simple test request
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Hello AI, this is GitHub Action test"
            }
        ]
    )

    # Print AI response
    print("\nAI Response:\n")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nERROR OCCURRED:")
    print(e)