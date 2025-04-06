import os
import pandas as pd
import tensorflow as tf
from transformers import BertTokenizer
from sklearn.preprocessing import LabelEncoder

MODEL_NAME = "bert-base-uncased"
MAX_LENGTH = 64
CSV_PATH = os.path.join(os.path.dirname(__file__), "training_data", "intent_data.csv")

def load_and_tokenize_data():
    df = pd.read_csv(CSV_PATH)

    label_encoder = LabelEncoder()
    df['label_encoded'] = label_encoder.fit_transform(df['label'])

    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

    encodings = tokenizer(
        list(df['text']),
        truncation=True,
        padding='max_length',
        max_length=MAX_LENGTH,
        return_tensors='tf'
    )

    labels = tf.convert_to_tensor(df['label_encoded'].values, dtype=tf.int32)

    dataset = tf.data.Dataset.from_tensor_slices((
        {
            "input_ids": encodings["input_ids"],
            "attention_mask": encodings["attention_mask"]
        },
        labels
    ))

    return dataset, label_encoder, tokenizer

if __name__ == '__main__':
    dataset, label_encoder, tokenizer = load_and_tokenize_data()
    print("Sample_batch: ")
    for batch in dataset.take(1):
        print(batch)