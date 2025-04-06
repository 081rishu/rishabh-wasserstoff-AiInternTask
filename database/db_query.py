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

if __name__ == "__main__":
    # fetch_all_emails() 
    fetch_cleaned_emails()
    # export_emails_to_csv() 