from email_integration.fetch_email import create_database, authenticate_gmail, fetch_and_store_emails
from model.data_cleaning import clean_and_store_emails
from model.email_summarizer import summarize_email
from context_understanding.intent_predictor import predict_intent
from context_understanding.intent_router import route_intent
from database.db_query import fetch_cleaned_emails

import sqlite3

DB_PATH = "database/email_data.db"

def get_latest_cleaned_email():
    """Fetch the latest cleaned email (by email_id) with recipient and subject."""
    query = """
        SELECT ce.cleaned_body, e.recipient, e.subject
        FROM cleaned_emails ce
        JOIN emails e ON ce.email_id = e.id
        ORDER BY ce.id DESC
        LIMIT 1
    """

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()

        if result:
            cleaned_body, recipient, subject = result
            print("\n Fetched latest cleaned email successfully.")
            return cleaned_body, recipient, subject
        else:
            print("\n No cleaned email found in the database.")
            return None, None, None

    except sqlite3.Error as e:
        print(f"\n SQLite Error: {e}")
        return None, None, None




def main():
    print("\n=== Step 1: Creating DB and Fetching Emails ===")
    create_database()
    service = authenticate_gmail()
    fetch_and_store_emails(service, max_results=1)

    print("\n=== Step 2: Cleaning Emails ===")
    clean_and_store_emails()

    print("\n=== Step 3: Checking Cleaned Emails ===")
    fetch_cleaned_emails()  # Debugging output

    text, to_email, subject = get_latest_cleaned_email()

    if not text:
        print("\nNo cleaned emails found. Exiting.")
        return

    print("\n=== Step 4: Summarizing and Predicting Intent ===")
    summary = summarize_email(text)
    intent = predict_intent(summary)

    print(f"\nSummary: {summary}")
    print(f"Predicted Intent: {intent}")

    print("\n=== Step 5: Routing Intent ===")
    result = route_intent(intent, summary, to_email=to_email, subject=subject)
    
    print("\n=== Final Output ===")
    print(result)


if __name__ == "__main__":
    main()