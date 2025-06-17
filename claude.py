#just for testing claude
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
)

print(message.content[0].text)