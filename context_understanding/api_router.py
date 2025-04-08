from fastapi import APIRouter
from database.db_query import fetch_cleaned_email_by_id
from context_understanding.intent_predictor import predict_intent
from context_understanding.intent_router import route_intent

router = APIRouter()

@router.get("/predict-intent/{email_id}")
def predict_intent_for_email(email_id: int):
    cleaned_text, subject, recipient = fetch_cleaned_email_by_id(email_id)

    if not cleaned_text:
        return {"error": f"No email found with id {email_id}"}

    intent = predict_intent(cleaned_text)
    action_result = route_intent(intent, cleaned_text, to_email=recipient, subject=subject)

    return {
        "email_id": email_id,
        "subject": subject,
        "recipient": recipient,
        "predicted_intent": intent,
        "action_result": action_result
    }
