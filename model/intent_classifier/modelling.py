import os
import sys
import joblib
import numpy as np
import tensorflow as tf
import tf2onnx
from sklearn.preprocessing import LabelEncoder
from transformers import TFBertModel, BertTokenizer, BertConfig
from tensorflow.keras.layers import Input, Dropout, Dense, Lambda  # type: ignore
from tensorflow.keras.models import Model  # type: ignore
from tensorflow.keras.optimizers import Adam  # type: ignore
from tensorflow.keras.losses import SparseCategoricalCrossentropy  # type: ignore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from preprocessing_data import load_and_tokenize_data

MODEL_NAME = 'bert-base-uncased'
MODEL_PATH = 'model/intent_classifier/model.keras'
ENCODER_PATH = 'model/intent_classifier/label_encoder.pkl'


def build_model(num_labels):
    config = BertConfig.from_pretrained(MODEL_NAME)
    config.hidden_act = "gelu_new"

    bert = TFBertModel.from_pretrained(MODEL_NAME, config=config)

    input_ids = Input(shape=(64,), dtype=tf.int32, name="input_ids")
    attention_mask = Input(shape=(64,), dtype=tf.int32, name="attention_mask")

    bert_output = Lambda(
        lambda x: bert(x[0], attention_mask=x[1]).last_hidden_state[:, 0, :],
        output_shape=(768,)
    )([input_ids, attention_mask])

    dropout = Dropout(0.3)(bert_output)
    output = Dense(num_labels, activation='softmax')(dropout)

    model = Model(inputs=[input_ids, attention_mask], outputs=output)

    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss=SparseCategoricalCrossentropy(from_logits=False),
        metrics=['accuracy']
    )

    return model


if __name__ == '__main__':
    dataset, label_encoder, tokenizer = load_and_tokenize_data()

    model = build_model(num_labels=len(label_encoder.classes_))

    # Train the model
    model.fit(dataset.batch(8), epochs=25)

    # Save the trained model
    model.save(MODEL_PATH)

    # Save the label encoder
    joblib.dump(label_encoder, ENCODER_PATH)

    # Export to ONNX
    spec = (
        tf.TensorSpec((None, 64), tf.int32, name="input_ids"),
        tf.TensorSpec((None, 64), tf.int32, name="attention_mask")
    )

    onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature=[spec], opset=13)

    onnx_path = "model/intent_classifier/model.onnx"
    with open(onnx_path, "wb") as f:
        f.write(onnx_model.SerializeToString())
