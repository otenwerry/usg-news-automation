#just for testing claude
import anthropic
import os
from datetime import datetime

now = datetime.now()
date = now.strftime("%B %d, %Y")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    #model="claude-sonnet-4-20250514",
    model="claude-3-5-haiku-20241022",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What is the top headline in the New York Times today?"
        }
    ],
    tools =[
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }
    ]
)

#print how many times was search used
if message.usage.server_tool_use.web_search_requests:
    print(f"Searched the web {message.usage.server_tool_use.web_search_requests} times")
else:
    print("Did not search the web")

#print the output
text_blocks = [block.text for block in message.content if block.type == "text"]
answer = " ".join(text_blocks)
print(answer)