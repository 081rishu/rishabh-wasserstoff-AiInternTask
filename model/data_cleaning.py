import re
import sqlite3
from database.database_utils import DB_FILE, get_email_id, insert_cleaned_email

def clean_text(text):
    '''basic text cleaning function that does:
        a) convert text to lowercase
        b) remove urls
        c) remove HTML tags
        d) remove special characters
        e) remove extra space between characters'''
    
    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', '', text)
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
    clean_and_store_emails()
    print("Data cleaning is done and cleaned email has been stored")