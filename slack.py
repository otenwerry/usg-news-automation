#send output into Slack.
#this file is separate for now to avoid spamming.

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

summary = "test"
#send the summary into Slack
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
