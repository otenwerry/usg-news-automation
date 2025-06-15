from openai import OpenAI
import os
import requests
from datetime import datetime, timedelta, timezone
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from newspaper import Article

now = datetime.now(timezone.utc)
yesterday = now - timedelta(days=1)

#get the news from Currents News API
currents_api_key = "iOHI4dun6qANBfRMMXt0mNDzOeitVzdATLSseLFLpO0HQCgH" #make this secret later

params = {
    "apiKey": currents_api_key,
    "language": "en",
    "start_date": yesterday.isoformat(),
    "end_date": now.isoformat(),
    "country": "US",
    "page_size": 200, #max is 200 allegedly, it seems you can do 300 but lets just go with it
    "page_number": 1
}

response = requests.get("https://api.currentsapi.services/v1/search", params=params)
data = response.json()

if data.get("status") != "ok":
    raise SystemExit(f"Currents API error: {data}")

articles = data.get("news", [])

print(len(articles))
for i, a in enumerate(articles):
    #print the given article info
    print(f"{i+1}. {a.get('title')}")
    print(a.get('description'))
    print(a.get('url'))
    print(a.get('published'))

    #try to print the full text
    try:
        article = Article(a.get('url'))
        article.download()
        article.parse()
        print(article.text)
    except Exception:
        print("Article could not be read")
    print("\n" + "-"*40 + "\n")




#have GPT look through these articles, pick the top k,
#and write a summary
'''
client = OpenAI(
    api_key = os.getenv("EIP_OPENAI_KEY")
)

#build a string of the articles
candidates = "\n".join([
    f"{i+1}. {a['title']} - {a['description']}"
    for i, a in enumerate(articles)
])

#write the prompt
prompt = f"""
Here are some recent news headlines about the United States government: {candidates}.
Your job is to pick the top 10 most important news stories, and write a summary of each.
To do so, use the following scoring system:
1. Impact: How big is this event's impact on the future of the United States government (0-5 points)
2. Trustworthiness: Is it from a trustworthy source? (0-2 points)
3. Novelty: Does it mention developments that are irregular or new, or regular events but 
of an usually large scale? (0-2 points)
4. Specificity: Does it report a concrete, specific outcome rather than something that's 
speculative or overly general? (0-2 points)
Calculate the total score and order the stories according to their score -- highest to 
lowest. For the top 10 stories, write a short justification for each component of your score, 
a few words in brackets behind the score. List your impact score last, and be more detailed here. 
Instead of brackets, use sub-bullets. Provide at least two bullets with pathways through which 
you could see the item to significantly impact wellbeing.
Return the list of stories, ordered as described above and each including the related 
hyperlink I originally shared.
"""

#get the summary
completion = client.chat.completions.create(
    model = "gpt-4o",
    messages = [{"role": "user", "content": prompt}]
)

summary = completion.choices[0].message.content
print(summary)

'''



#send the summary into Slack
'''
client = WebClient(token=os.getenv("EIP_SLACK_TOKEN"))
channel_id = os.getenv("EIP_SLACK_CHANNEL_ID")

try:
    client.chat_postMessage(
        channel=channel_id,
        text=summary
    )
except SlackApiError as e:
    print(f"Slack API error: {e}")
    raise
'''










#old: NewsAPI call
#get the daily news into a list of articles
'''
news_API_key = "846c21604d134a28a4a2c125f67488fe"
params = {
    "apiKey": news_API_key,
    "from": yesterday.isoformat(),
    "to": now.isoformat(),
    "sortBy": "publishedAt", #publishedAt, popularity, relevancy
    "country": "us",
    "language": "en",
    "pageSize": 100,
}

response = requests.get("https://newsapi.org/v2/top-headlines", params=params)
#response = requests.get("https://newsapi.org/v2/everything", params=params)
data = response.json()

if response.status_code != 200:
    print(f"HTTP error {response.status_code}: {data.get('message')}")
    raise SystemExit(1)
if data.get("status") != "ok":
    print(f"NewsAPI error: {data.get('code')} – {data.get('message')}")
    raise SystemExit(1)

articles = data.get("articles", [])

#print stuff out to check

print(len(articles))

for article in articles:
    print(article["title"])
    print(article["description"])
    print(article["url"])
    print(article["publishedAt"])
    print(article["source"]["name"])



#print the full first article
print("\n\n...\n\n")

article = Article(articles[0]["url"])
article.download()
article.parse()
print(article.text)'''