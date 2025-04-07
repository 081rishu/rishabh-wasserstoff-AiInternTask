import re
import sqlite3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.database_utils import DB_FILE, get_email_id, insert_cleaned_email, create_database, clear_cleaned_emails_table
from bs4 import BeautifulSoup

def clean_text(text):
    """Clean and normalize email body text."""
    soup = BeautifulSoup(text, "html.parser")
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    text = soup.get_text(separator=" ")

    text = re.sub(r'\b(?:fontfamily|fontstyle|padding|margin|width|height|important|glassdoor|srcurlformat)\w*\b', '', text, flags=re.IGNORECASE)

    text = re.sub(r'https?://\S+|www\.\S+', '', text)  
    text = re.sub(r'\S+@\S+', '', text)               
    text = re.sub(r'[^\w\s.,!?-]', '', text)       

    text = re.sub(r'\s+', ' ', text).strip()

    return text


def clean_and_store_emails():
    '''
    - fetch raw emails,
    - extract text and apply clean_text function and 
    - store then into claned email table using insert_cleaned_email
    '''

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT message_id, sender, recipient, subject, body, timestamp FROM emails")
    rows = cursor.fetchall()

    for row in rows:
        message_id, sender, recipient, subject, body, timestamp = row

        cleaned_body = clean_text(body)

        email_id = get_email_id(conn, message_id)

        if email_id:
            insert_cleaned_email(conn, email_id, sender, recipient, subject, timestamp, cleaned_body)
    conn.close()
    
if __name__ == "__main__":
    clear_cleaned_emails_table()
    clean_and_store_emails()
    print("Data cleaning is done and cleaned email has been stored")