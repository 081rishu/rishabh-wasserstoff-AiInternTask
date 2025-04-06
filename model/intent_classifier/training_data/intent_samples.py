import pandas as pd
import os

data = {
    "SummaryRequest" : ["Can you summarize the conversation we had with the client last week?",
                        "Please provide a brief overview of this email thread.",
                        "Could you send me a summary of the attached discussion?",
                        "I don’t have time to go through all emails. What’s the gist?",
                        "Give me a TL;DR of the project update mails.",
                        "Can you quickly recap what this email thread is about?",
                        "Need a summary of the previous messages before the meeting.",
                        "What are the key points from this conversation?",
                        "Please highlight the most important details from this exchange.",
                        "I want a quick summary of the main updates discussed here."],

    "InfoRequest" :    ["Can you tell me the deadline for the submission?",
                        "What is the current status of the project?",
                        "I need the login credentials for the dashboard.",
                        "Please share the client’s contact details.",
                        "Can you send the latest sales report?",
                        "What are the prerequisites for the training session?",
                        "Could you provide more details on the pricing?",
                        "Do we have any updates from the legal team?",
                        "I’m looking for the documentation on the new API.",
                        "Where can I find the files for last week’s presentation?"],

    "WebSearch" : ["Can you find the latest news on the NVIDIA stock performance?",
                    "What’s the weather forecast for New York this weekend?",
                    "Look up top-rated productivity tools for remote teams.",
                    "Can you find tutorials on integrating Stripe with FastAPI?",
                    "Please get me recent articles on AI regulation in the EU.",
                    "Find out who won the Best Picture at the Oscars this year.",
                    "Can you check train timings from Delhi to Jaipur for tomorrow?",
                    "Search for reviews on the new iPad Pro 2025 model.",
                    "What are the visa requirements for traveling to Canada from India?",
                    "Get a list of upcoming tech conferences in Asia."],

    "SlackForward" : [  "This update needs to go to the dev team on Slack ASAP.",
                        "Can you post this announcement in our general Slack channel?",
                        "Please share this security alert with the IT group on Slack.",
                        "Kindly notify the design team on Slack about the new changes.",
                        "Forward this bug report to the #qa Slack channel.",
                        "Push this weekly summary to Slack so the team stays updated.",
                        "This urgent request should be posted in the incident-response channel.",
                        "Share this client feedback with the product team on Slack.",
                        "Please drop this reminder message in the team chat.",
                        "Alert the operations team via Slack that the server went down."],

    "MeetingScheduling" : ["Can we schedule a meeting to discuss the new feature rollout?",
                            "Let's have a call on Wednesday to go over the proposal.",
                            "Are you available Friday afternoon for a quick sync?",
                            "I'd like to set up a meeting next week to finalize the budget.",
                            "Please arrange a Zoom meeting for the whole team tomorrow.",
                            "How about we meet on Monday at 10 AM to review the report?",
                            "Schedule a call with the vendor sometime this week.",
                            "Can we block 30 minutes on your calendar for a strategy discussion?",
                            "Let's connect over a video call to plan the roadmap.",
                            "Please propose a few time slots for a project kickoff meeting."],

    "CalenderEvent" : ["The client demo is confirmed for Thursday at 3 PM. Please add it to the calendar.",
                        "Mark your calendar for the quarterly review on May 15th at 11:00 AM.",
                        "I've booked a room for our training session on Tuesday, 2 PM.",
                        "Please log the upcoming workshop scheduled for April 20th.",
                        "We’re attending the security webinar on Friday. Add it to the team calendar.",
                        "Don't forget the HR orientation event on Monday morning.",
                        "The tech talk is happening on June 5th. Kindly add the event to our calendar.",
                        "Our annual planning session is fixed for next Thursday at 9 AM.",
                        "Add the new hire onboarding event scheduled for next Tuesday.",
                        "Reminder: The performance review meeting is set for April 30th at 10 AM."],

    "AutomatedReply" : ["Could you please send me the updated invoice for this month?",
                        "Let me know once you’ve received the documents.",
                        "Thanks for your help on this!",
                        "Please confirm if the meeting invite was sent.",
                        "Can you share the details again?",
                        "I have submitted the form as requested.",
                        "Kindly acknowledge receipt of the package.",
                        "Following up on my previous email regarding access to the portal.",
                        "Let me know if there's anything else you need from me.",
                        "Thank you for the update."],
    
    "Others" : ["Hope you’re doing well! Just wanted to check in.",
                "Here’s the monthly newsletter from our team.",
                "We are excited to announce our new product launch!",
                "This is a system-generated message. No reply needed.",
                "Friendly reminder: the office will be closed on Friday.",
                "Please find attached the latest version of the handbook.",
                "Congratulations on completing your first year with us!",
                "Here are the notes from today’s internal discussion.",
                "Thank you all for your hard work this quarter.",
                "We've updated our terms of service."]
}


rows = [(text, label) for label, samples in data.items() for text in samples]

df = pd.DataFrame(rows, columns=["text", "label"])
# csv_path = "intent_classifier/training_data/intent_samples.csv"
base_dir = os.path.dirname(__file__)
csv_path =  os.path.join(base_dir, "intent_data.csv")
df.to_csv(csv_path, index=False)