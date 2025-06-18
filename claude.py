import anthropic
import os
from datetime import datetime

#claude needs search to find date, so we pass
#it in manually to save a search
now = datetime.now()
date = now.strftime("%B %d, %Y")
time = now.strftime("%H:%M:%S")

#read in the prompt from prompt.txt
with open("prompt.txt", "r") as file:
    prompt = file.read()

prompt = prompt.format(date=date, time=time)

#summon claude and give it the prompt
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    #model="claude-3-5-haiku-20241022",
    #figure out what to set max_tokens to. 
    #too low and it will cut off, too high and it will be expensive
    max_tokens=5000, 
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

#print the output
text_blocks = [block.text for block in message.content if block.type == "text"]
answer = " ".join(text_blocks)
print(answer)