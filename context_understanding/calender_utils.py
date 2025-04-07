import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    token_path = os.path.join(base_dir, "authentication", "token.json")
    creds_path = os.path.join(base_dir, "authentication", "credentials.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_calendar_event(summary, start_time, duration_minutes=30, attendees_emails=[]):
    service = get_calendar_service()

    start_datetime = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    end_datetime = start_datetime + timedelta(minutes=duration_minutes)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata'
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata'
        },
        'attendees': [{'email': email} for email in attendees_emails]
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event

if __name__ == '__main__':
    title = "Project Meeting"
    start_time = "2025-04-07T14:30:00"  # ISO format
    duration = 45
    attendees = ["someone@example.com"]

    event = create_calendar_event(title, start_time, duration, attendees)
    print("Event created:", event.get('htmlLink'))