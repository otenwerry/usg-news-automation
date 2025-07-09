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
client = anthropic.Anthropic(api_key=os.getenv("EIP_ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    #model="claude-3-5-haiku-20241022",
    max_tokens=5000, #tends to put out ~3k tokens, and this parameter is required, so we overestimate
    temperature=0,
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

#get the full text of the output, avoiding the search tool blocks
full_text = ""
for block in message.content:
    if block.type == "text":
        full_text += block.text

#start from the answer header, if possible
if "## Answer" in full_text:
    answer_start = full_text.index("## Answer") + len("## Answer")
    answer = full_text[answer_start:].strip()
else:
    answer = full_text

print(answer)
print("-"*100)
print(full_text)