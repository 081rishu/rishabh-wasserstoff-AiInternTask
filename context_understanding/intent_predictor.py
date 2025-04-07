import os
import joblib 
import numpy as np
import onnxruntime as rt
from transformers import BertTokenizer
from intent_router import route_intent

MODEL_DIR = os.path.join("model", "intent_classifier")
ONNX_MODEL_PATH = os.path.join(MODEL_DIR, "model.onnx")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")
MODEL_NAME = 'bert-base-uncased'
MAX_LEN = 64

tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
label_encoder = joblib.load(ENCODER_PATH)

session = rt.InferenceSession(ONNX_MODEL_PATH, providers=['CPUExecutionProvider'])

def predict_intent(summary:str) -> str:
    inputs = tokenizer(
            summary,
            padding='max_length',
            truncation=True,
            max_length=MAX_LEN,
            return_tensors='np'
    )
    inputs = {k: v.astype(np.int32) for k, v in inputs.items() if k in ['input_ids', 'attention_mask']}

    outputs = session.run(None, inputs)
    predictions = np.argmax(outputs[0], axis=1)
    predicted_label = label_encoder.inverse_transform(predictions)[0]

    return predicted_label

if __name__ == "__main__":
    email_summary = " slack on channel"
    intent = predict_intent(email_summary)
    print(f"Predicted Intent: {intent}")
    
    route_intent(intent, email_summary)