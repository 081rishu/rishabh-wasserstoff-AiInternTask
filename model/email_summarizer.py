from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer
import tensorflow as tf

## load model
MODEL_NAME = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = TFAutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def summarize_email(email_body, max_input_length=512, max_output_length=100):
    ''' generate summary from a cleaned email_body'''

    input_text = "summarize: " + email_body.strip().replace("\n", " ")

    # tokenize input
    inputs = tokenizer(
            input_text,
            return_tensors='tf',
            max_length=max_input_length,
            truncation=True,
            padding='max_length'
    )

    ## generated summary as output
    output = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=max_output_length,
            num_beams=4,
            early_stopping=True
    )

    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return summary


# email_body = """
# Dear team,

# I hope this message finds you well. I wanted to follow up on our last meeting regarding the Q2 product launch timeline.
# Please ensure that all feedback from QA is addressed by Friday. We'll sync again on Monday.

# Best,
# Product Manager
# """

# summary = summarize_email(email_body)
# print("Summary:", summary)



# '''
# HSJB Global is hiring Jobs Your job listings for 3 April 2025 Data Scientist Cochin HSJB Global AIML Engineers Cochin 18L - 20L Employer Est. Easy Apply Tech Meridian Academy AI with Machine learning Trainer Cochin 18K - 25K Employer Est. Easy Apply RP2 Data Science Intern Cochin 10K Employer Est. Easy Apply MathLab Research AI Chemistry Research Internship Pattern Recognition in Chemical Industry Datasets Cochin 5K - 8K Employer Est. Easy Apply Beat Center of Excellence Data AnalyticsTrainer Thrissur 22K Employer Est. Easy Apply See more jobs Want more listings like these? Similar jobs can have different titles. Create job alerts for related roles. data engineer Create quantitative researcher Create quantitative analyst Create Looking for something a little different? You can edit your job alert here. Data Scientist Cochin Sent Daily Edit This message was sent to Privacy Policy Manage Settings Unsubscribe 2261 Market Street STE 10389, San Francisco, CA 94114 Copyright 2008-2025, LLC. , Worklife Pro, Bowls and logo are proprietary trademarks of LLC.
# '''

# '''
# If youre reading this youre just in time. Savings on select courses end tonight. Udemy Udemy Sale ends tonight New skills are within your reach and courses are now sale. Shop now Check out the top new courses Five Core Meditations For Spirit Guides Five Core Meditations For Spirit Guides 5 3 Test AI LLM App with DeepEval, RAGAs more using Ollama Test AI LLM App with DeepEval, RAGAs more using Ollama 5 4 Master NotebookLM Perplexity GenAI to Boost Productivity Master NotebookLM Perplexity GenAI to Boost Productivity 4.93 7 Students who enrolled in 2025 Deploy ML Model in Production with FastAPI and Docker also enrolled in 2025 Deploy ML Model in Production with FastAPI and Docker 2025 Deploy ML Model in Production with FastAPI and Docker 4.7 522 MLflow in Action - Master the art of MLOps using MLflow tool MLflow in Action - Master the art of MLOps using MLflow tool 4.43 740 ML in Production From Data Scientist to ML Engineer ML in Production From Data Scientist to ML Engineer 4.61 191 Get started with top categories Development Development Development IT Software IT Software IT Software Business Business Business Development Lifestyle Lifestyle IT Software Design Design Business Music Music Udemy Udemy Udemy Udemy Trusted by top organizations Thousands of businesses around the world count on Udemy to upskill their employees. Explore courses Udemy Logo The power of possibilities Download our app and learn anywhere apple apple Instagram About us Udemy Business You are receiving this email because you signed up on Udemy.com with this email address. Please do not reply to this unmonitored email account. Visit the help center for questions and support. Manage preferences Support Unsubscribe Privacy terms Udemy, 600 Harrison Street, 3rd floor, San Francisco, CA 94107 Some exclusions apply. Coupon code expires 2025-04-04.
# '''