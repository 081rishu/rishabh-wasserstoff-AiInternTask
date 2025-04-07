import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

client = WebClient(token=SLACK_BOT_TOKEN)

def send_slack_message(message: str):
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            text=message
        )
        print("Message forwarded in slack channel")
        return response["message"]["text"]
    except SlackApiError as e:
        print(f"Slack APi error:{e.response['error']}")
        return None
    
if __name__ == '__main__':
    summary = "Reminder: Submit the client report by 5 PM today."
    send_slack_message(summary)