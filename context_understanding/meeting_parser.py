import re
from dateutil import parser as date_parser
from datetime import datetime, timedelta

def parse_meeting_details(summary):
    attendees = re.findall(r'[\w\.-]+@[\w\.-]+', summary)

    duration_match = re.search(r'(\d+)\s*(minutes|min)', summary, re.IGNORECASE)
    duration = int(duration_match.group(1)) if duration_match else 30

    try:
        start_time_obj = date_parser.parse(summary, fuzzy=True)
        start_time = start_time_obj.strftime('%Y-%m-%dT%H:%M:%S')
    except:
        start_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    title_match = re.search(r'titled\s*["“]?(.+?)["”]?(?:\s+with|\s+at|\s+on|\s+for|$)', summary, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Scheduled Meeting"

    return title, start_time, duration, attendees