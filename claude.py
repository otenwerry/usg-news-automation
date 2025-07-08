import anthropic
import os
from datetime import datetime

#claude needs search to find date, so we pass
#it in manually to save a search
now = datetime.now()
date = now.strftime("%B %d, %Y")
time = now.strftime("%H:%M:%S")

#read in the prompts and pass in the date and time
with open("prompt.txt", "r") as file:
    prompt = file.read()
prompt = prompt.format(date=date, time=time)

with open("system_prompt.txt", "r") as file:
    system_prompt = file.read()

#summon claude and give it the prompt
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    #model="claude-3-5-haiku-20241022",
    max_tokens=5000, #tends to put out ~3k tokens, and this parameter is required, so we overestimate
    system=system_prompt,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    tools =[
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 10
        }
    ]
)

#print how many times was search used
if message.usage.server_tool_use.web_search_requests:
    print(f"Searched the web {message.usage.server_tool_use.web_search_requests} times")
else:
    print("Did not search the web")

#find the last tool use
last_tool_index = -1
for i, block in enumerate(message.content):
    if block.type == "tool_use":
        last_tool_index = i

#THIS PART ISN'T WORKING
#collect text blocks after the last tool use.
#these are the answer blocks; the text before is more of chain-of-thought
if last_tool_index >= 0:
    answer_blocks = [block.text for block in message.content[last_tool_index + 1:] if block.type == "text"]
else:
    answer_blocks = [block.text for block in message.content if block.type == "text"]

#join the answer blocks into a single string and print
answer = " ".join(answer_blocks)
print(answer)