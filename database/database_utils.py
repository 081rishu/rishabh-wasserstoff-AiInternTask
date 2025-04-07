import sqlite3

DB_FILE = 'database/email_data.db'

def create_database():
    '''create a sqlite database containing tables'''
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    '''table to store raw data from email'''
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id  TEXT UNIQUE,
            thread_id TEXT,
            sender TEXT,
            recipient TEXT,
            subject TEXT,
            body TEXT,
            timestamp TEXT
        )
    """)

    '''table to strore processed data of email'''
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cleaned_emails(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id INTEGER UNIQUE,  
            sender TEXT,
            recipient TEXT,
            subject TEXT,
            timestamp TEXT,
            cleaned_body TEXT,
            FOREIGN KEY (email_id) REFERENCES emails(id)
        )
    """)

    '''table to store summarized emails with email.id as foreign key'''
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summarized_emails(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id INTEGER NOT NULL,
            summary TEXT NOT NULL,
            summarized_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (email_id) REFERENCES emails(id) ON DELETE CASCADE          
        )
    """)

    '''table to store predicted intent with email.id as a foreing key'''
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intent_predictions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id INTEGER NOT NULL,
            intent_label TEXT NOT NULL,
            confidence_score REAL,
            predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (email_id) REFERENCES emails(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()

def insert_email(message_id, thread_id, sender, recipient, subject, body, timestamp):
    '''insert email data into the database'''
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO emails(message_id, thread_id, sender, recipient, subject, body, timestamp)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (message_id, thread_id, sender, recipient, subject, body, timestamp))

        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Email {message_id} already exist in the database")

    conn.close()


def get_email_id(conn, message_id):
    """Fetch the email ID from the emails table using the message_id."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM emails WHERE message_id = ?", (message_id,))
    result = cursor.fetchone()
    return result[0] if result else None



def insert_cleaned_email(conn, email_id, sender, recipient, subject, timestamp, cleaned_body):
    """Insert a cleaned email into the cleaned_emails table."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cleaned_emails (email_id, sender, recipient, subject, timestamp, cleaned_body)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(email_id) DO NOTHING
    """, (email_id, sender, recipient, subject, timestamp, cleaned_body))
    conn.commit()


def clear_cleaned_emails_table(db_path="database/email_data.db"):
    """
    Deletes all records from the cleaned_emails table.
    Useful for re-running the cleaning pipeline with updated logic.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cleaned_emails")
        conn.commit()
        print("All records from 'cleaned_emails' table have been deleted.")

    except sqlite3.Error as e:
        print(f"Error while clearing table: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    clear_cleaned_emails_table()