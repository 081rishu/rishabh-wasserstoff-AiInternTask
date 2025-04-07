import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pickle
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from database.database_utils import create_database, insert_email

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = "authentication/credentials.json"
TOKEN_FILE = "authentication/token.pickle"

# Gmail API Scope (Read Emails)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.compose'
]

def authenticate_gmail():
    creds = None

    # Load existing credentials
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    # Refresh or request new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the new credentials
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)  


def fetch_and_store_emails(service, max_results=5):
    """Fetch the latest emails and store them in the database."""
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = results.get("messages", [])

    if not messages:
        print("No new emails found.")
        return

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]

        # Extract required email details
        message_id = msg["id"]
        thread_id = msg_data["threadId"]
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
        recipient = next((h["value"] for h in headers if h["name"] == "To"), "Unknown")
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        timestamp = msg_data["internalDate"]
        body = extract_email_body(msg_data)

        # Store in database
        insert_email(message_id, thread_id, sender, recipient, subject, body, timestamp)

        print(f"\nStored Email - Subject: {subject} | From: {sender}")
        

def extract_email_body(msg_data):
    """Extract email body from the message payload."""
    body = ""
    if "parts" in msg_data["payload"]:
        for part in msg_data["payload"]["parts"]:
            if part["mimeType"] == "text/plain":
                body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                break
    else:
        body = base64.urlsafe_b64decode(msg_data["payload"]["body"]["data"]).decode("utf-8")
    return body

if __name__ == "__main__":
    create_database()
    service = authenticate_gmail()
    fetch_and_store_emails(service, max_results=1)