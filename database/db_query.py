'''this script is solely to check the content of the eamil_data.db'''

import sqlite3
import pandas as pd

DATABASE_PATH = "database/email_data.db"

def fetch_all_emails():
    """Fetch and display all emails in a readable format."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Fetch all stored emails
    cursor.execute("SELECT * FROM emails")
    rows = cursor.fetchall()

    if not rows:
        print("No emails found in the database.")
        return

    # Get column names
    columns = [description[0] for description in cursor.description]

    # Print emails in a structured format
    for row in rows:
        email_dict = dict(zip(columns, row))
        print("\n--- Email Record ---")
        for key, value in email_dict.items():
            print(f"{key}: {value}")

    conn.close()


def fetch_cleaned_emails():
    """Fetch and display all cleaned emails in a readable format."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM cleaned_emails")
        rows = cursor.fetchall()

        if not rows:
            print("\nNo cleaned emails found in the database.")
            return

        # Get column names
        columns = [description[0] for description in cursor.description]

        # Print cleaned emails
        for row in rows:
            cleaned_email = dict(zip(columns, row))
            print("\n--- Cleaned Email Record ---")
            for key, value in cleaned_email.items():
                print(f"{key}: {value}")
    except sqlite3.OperationalError:
        print("\nThe table 'cleaned_emails' does not exist yet.")
    
    conn.close()



def export_emails_to_csv(filename="emails.csv"):
    """Export all emails from the database to a CSV file."""
    conn = sqlite3.connect(DATABASE_PATH)
    
    try:
        df = pd.read_sql_query("SELECT * FROM emails", conn)
        df.to_csv(filename, index=False)
        print(f"Emails successfully exported to {filename}")
    except Exception as e:
        print(f"Error exporting emails: {e}")
    
    conn.close()


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
        with sqlite3.connect(DATABASE_PATH) as conn:
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
    
    
def fetch_cleaned_email_by_id(email_id: int):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT body, subject, recipient FROM emails WHERE id = ?", (email_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        body, subject, recipient = result

        # Optional cleaning
        cleaned_body = body.strip().replace("\n", " ")  # Basic cleaning

        return cleaned_body, subject, recipient
    else:
        raise ValueError(f"No email found with ID: {email_id}")



if __name__ == "__main__":
    # fetch_all_emails() 
    fetch_cleaned_emails()
    # export_emails_to_csv() 