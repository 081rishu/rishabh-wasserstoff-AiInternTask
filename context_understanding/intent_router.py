import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from calender_utils import create_calendar_event
from meeting_parser import parse_meeting_details
from datetime import datetime
from slack_utils import send_slack_message
from websearch_utils import perform_web_search
from reply_generator import generate_reply, create_draft
from email_integration.fetch_email import authenticate_gmail 

def route_intent(intent:str, summary: str, to_email: str = None, subject: str = "Re: Your email"):
    print(f"Intent: {intent}")
    
    if intent == "SummaryRequest":
        print("Summary Requested : ")
        return summary

    # elif intent == "InfoRequest":
    #     print("Information Request detected")
    #     # to trigger information extraction

    elif intent == "WebSearch":
        print("Performing web search...")
        results = perform_web_search(summary)
        print("Search Results:\n", results)

    elif intent == "SlackForward":
        print("Forwarding message to Slack...")
        send_slack_message(summary)

    elif intent == "SceduledEvent":
        try:
            title, start_time, duration, attendees = parse_meeting_details(summary)
            event = create_calendar_event(title, start_time, duration, attendees)
            return f"Calendar event created: {event.get('htmlLink')}"
        except Exception as e:
            return f"Failed to create event: {str(e)}"

    elif intent == "AutomatedReply":
        print("Generating automated reply...")
        try:
            reply = generate_reply(summary)
            print("Draft reply:\n", reply)

            if to_email:  
                service = authenticate_gmail()
                draft = create_draft(service, 'me', reply, to_email, subject)
                return f"Reply drafted successfully with ID: {draft.get('id')}"
            else:
                return reply  
        except Exception as e:
            return f"Failed to generate automated reply: {str(e)}"
    else:
        print("Nothing needed to be done")
        #for others class


if __name__ == '__main__':
    intent = 'SceduledEvent'
    summary = "Schedule a meeting titled Team Sync with jane@example.com at 4:15 PM on April 7th for 45 minutes."
    result = route_intent(intent, summary)
    print(result)