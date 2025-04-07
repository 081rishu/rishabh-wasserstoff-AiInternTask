# AI-Powered Personal Email Assistant

An intelligent email assistant that connects to your Gmail inbox, understands the context of incoming emails using language models, stores structured data in a database, and automates actions like web searches, Slack notifications, calendar scheduling, and drafting replies — all based on the intent detected from the email content.


## Features

- Gmail Integration (via Gmail API with OAuth 2.0 authentication)
- Email Parsing and Storage in SQLite database
- Intent Detection using a Transformer-based BERT model
- Google Calendar Event Creation (via Google Calendar API)
- Slack Message Forwarding (via Slack Web API with a Slack Bot Token)
- Web Search Integration (using SerpAPI for Google Search)
- Automated Reply Generation as Draft (using Flan-T5 via Hugging Face Transformers + Gmail API)


## Project Structure

wasserstoff
    ├── authentication
    │   ├── credentials.json
    │   ├── token.pickle
    │
    ├── context_understanding
    │   ├── calendar_utils.py
    │   ├── intent_predictor.py
    │   ├── intent_router.py
    │   ├── meeting_parser.py
    │   ├── reply_generator.py
    │   ├── slack_utils.py
    │   └── websearch_utils.py
    │
    ├── database
    │   ├── database_utils.py
    │   ├── db_query.py
    │   └── email_data.db
    │   
    ├── email_integration
    │   └── fetch_email.py
    │   
    ├── model
    │   ├── intent_classifier
    │   │   ├── training_data
    │   │   │   ├── intent_data.csv
    │   │   │   └── intent_samples.py
    │   │   │
    │   │   ├── label_encoder.pkl
    │   │   ├── model.keras
    │   │   ├── model.onnx
    │   │   ├── modelling.py
    │   │   └── preprocessing_data.py
    │   │
    │   ├── data_cleaning.py
    │   └── email_summarizer.py
    │
    ├── venv
    ├── .env  
    ├── .gitignore 
    ├── main.py
    ├── README.md
    └── requirements.txt


## Getting Started

Follow these steps to set up the project on your local machine:

1. Clone the Repository:
    - git clone https://github.com/081rishu/rishabh-wasserstoff-AiInternTask.git
    - cd rishabh-wasserstoff-AiInternTask

2. Create and Activate Virtual Environment (optional but recommended)
    - python -m venv venv
    - venv\Scripts\activate

3. Install Dependencies
    - pip install -r requirements.txt

4. Add Gmail API Credentials
    - Go to the Google Cloud Console (https://console.cloud.google.com/)
    - Create a new project or select an existing one.
    - Enable the Gmail API and Google Calendar API.
    - Go to APIs & Services > Credentials.
    - Click Create Credentials > OAuth client ID.
    - Choose Desktop App, and download the credentials.json file.
    - Place the downloaded credentials.json inside the authentication/ directory.

    The first time you run the app, it will open a browser window to authenticate with your Google account and generate a token.pickle file for future use. Save that token.pickle inside the authentication/ directory as well.

5. Setup Environment Variables
    Create a .env file in the root directory and add the following:
        - SERPAPI_API_KEY=<your-serpapi-key>
        - SLACK_BOT_TOKEN=<your-slack-bot-token>
        - SLACK_CHANNEL_ID=<your-slack-channer-id>


## Usage
After setup, you can run the assistant by executing the main script:
    - python main.py

What Happens on Running:
    - Email Fetching:
        Connects to your Gmail inbox using the Gmail API and fetches new emails.

    - Parsing and Storage:
        Extracts sender, recipient, subject, timestamp, body, and stores them in an SQLite database (email_data.db).

    - Intent Detection:
        Uses a fine-tuned BERT-based model to classify each email into predefined intent categories:
            -SummaryRequest
            -WebSearch
            -SlackForward
            -SceduledEvent
            -AutomatedReply
            -Others

    - Context-Aware Actions:
        Based on the intent, the assistant performs actions like:
            Scheduling calendar events via Google Calendar API
            Forwarding emails as Slack messages using Slack API
            Running web searches with SerpAPI
            Generating intelligent reply drafts using Flan-T5

    - Logging / Output:
        Key steps and actions taken by the assistant are logged to the console for transparency and debugging.

<pre> ```mermaid flowchart TD A[Gmail Inbox]:::input --> B[fetch_email.py<br>Authenticate + Fetch Emails (OAuth2)] B --> C[data_cleaning.py<br>Clean + Structure Email Text] C --> D[email_data.db<br>(SQLite Database)] D --> E[email_summarizer.py<br>Summarize Email (Flan-T5)] D --> F[intent_predictor.py<br>Predict Intent (BERT)] E --> G[intent_router.py<br>Decide Action based on Intent] F --> G G --> H[calendar_utils.py<br>Google Calendar Event] G --> I[slack_utils.py<br>Send to Slack Channel] G --> J[websearch_utils.py<br>Search Web (SerpAPI)] G --> K[reply_generator.py<br>Generate Reply Draft] classDef input fill:#dff,stroke:#00f; ``` </pre>


## Intent_Prediction Model:
    Model Taining :
    -Dataset: 50 examples per class, balanced across 7 intent classes.
    -Tokenizer: BERT tokenizer with max length = 64.
    -Model: Transformer-based BERT model fine-tuned using TensorFlow.
    - Output Format: Saved in both .keras and .onnx for flexibility and performance.

    This model takes email summary as input and given the intent as output based on which the further action is taken.