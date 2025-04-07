from calender_utils import create_calendar_event
from meeting_parser import parse_meeting_details
from datetime import datetime
from slack_utils import send_slack_message
from websearch_utils import perform_web_search


def route_intent(intent:str, summary: str):
    print(f"Intent: {intent}")
    
    if intent == "SummaryRequest":
        print("Summary Requested : ")
        # to return summary directly from the db

    elif intent == "InfoRequest":
        print("Information Request detected")
        # to trigger information extraction

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
        print("some response to be sent")
        ## generate a draft

    else:
        print("Nothing needed to be done")
        #for others class


if __name__ == '__main__':
    intent = 'SceduledEvent'
    summary = "Schedule a meeting titled Team Sync with jane@example.com at 4:15 PM on April 7th for 45 minutes."
    result = route_intent(intent, summary)
    print(result)