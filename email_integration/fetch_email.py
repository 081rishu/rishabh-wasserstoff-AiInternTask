import os
import pickle
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# File paths
CREDENTIALS_FILE = "authentication/credentials.json"
TOKEN_FILE = "authentication/token.pickle"

# Gmail API Scope (Read Emails)
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

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

    
    service = build("gmail", "v1", credentials=creds)
    return service  

def fetch_emails(service, max_results=5):
    """Fetch the latest emails from the inbox."""
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = results.get("messages", [])

    if not messages:
        print("No new emails found.")
        return

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]

        # Extract required email details
        email_data = {
            "id": msg["id"],
            "sender": next((h["value"] for h in headers if h["name"] == "From"), "Unknown"),
            "subject": next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject"),
            "body": extract_email_body(msg_data),
        }

        print("\n--- Email ---")
        print(f"From: {email_data['sender']}")
        print(f"Subject: {email_data['subject']}")
        print(f"Body: {email_data['body'][:200]}...")  # Print first 200 characters

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
    service = authenticate_gmail()
    fetch_emails(service, max_results=10)