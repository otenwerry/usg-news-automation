import anthropic
import os
from datetime import datetime

#claude needs search to find date, so we pass
#it in manually to save a search
now = datetime.now()
date = now.strftime("%B %d, %Y")
time = now.strftime("%H:%M:%S")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

prompt = f"""
It is currently {date} at {time} Eastern. 
Your job is to compile a list of the most significant news developments surrounding 
the US government that have occurred in the last 24 hours. Use various sources to 
identify news stories: academic outlets, trustworthy aggregators like Reuters and 
AP, social media like X, and analysis sites like think tanks.

First, put together 10 articles that seem highly relevant at a first glance. 
Then, pick the 5 articles out of these with the highest scores out of 11 using 
the following criteria:
Impact (0-5 points): How impactful is this event? We’re ultimately interested 
in well-being, measured in wellbeing-adjusted life years (WELLBYs); we’re also 
instrumentally interested in big changes in the US government, as an institution 
with strong influence over global well-being. Elaborate with 1-2 bullet points 
about the event’s expected impact on either or both.
Trustworthiness (0-2 points): how trustworthy is the source? Do not elaborate.
Novelty (0-2 points): are the events mentioned new, irregular, or of an unusually 
large scale? Do not elaborate.
Specificity (0-2 points): does it report a concrete, specific event? Do not elaborate.

For each story you identify, first list the title, date & time in Eastern, 
and source link, all in one line. Then, on the next line, write a 1-sentence summary. 
Then give the scores, as well as the elaboration on the impact score. For example:
Article 1: Trump Administration Seeks to…, May 8, 2025 at 4:32 pm, https://...
This article describes the Trump administration’s attempt to…
Total score: 8/11
Impact: 4/5
[Elaboration]
Trustworthiness: 2/2
Novelty: 1/2
Specificity: 1/2
"""

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