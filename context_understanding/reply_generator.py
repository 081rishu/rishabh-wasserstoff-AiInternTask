import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from transformers import pipeline

from email_integration.fetch_email import authenticate_gmail 

reply_generator = pipeline("text2text-generation", model="google/flan-t5-base")

def generate_reply(email_text: str) -> str:
    prompt = (
        "You are the recipient of the following email. Generate a response to this email. "
        "Write a clear and concise reply in first person. Maintain a natural, professional tone. "
        "Assume you understand the context and avoid repeating the original email unnecessarily. "
        "Be helpful and relevant based on the content. \n\n"
        f"Email:\n\"{email_text}\"\n\n"
        "Reply:"
    )

    response = reply_generator(prompt, max_length=150, do_sample=True, temperature=0.7)
    return response[0]["generated_text"]

def create_draft(service, user_id: str, message_body: str, to: str, subject: str):
    message = MIMEText(message_body)
    message['to'] = to
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'message': {
            'raw': raw_message
        }
    }

    draft = service.users().drafts().create(userId=user_id, body=create_message).execute()
    print(f"Draft created. ID: {draft['id']}")
    return draft

def main():
    email_text = "Hi Rishabh, could you please send me the updated report by EOD today?"
    to_email = "john@example.com"
    subject = "Re: Updated Report"

    reply = generate_reply(email_text)

    service = authenticate_gmail()  
    create_draft(service, 'me', reply, to_email, subject)

if __name__ == '__main__':
    main()
