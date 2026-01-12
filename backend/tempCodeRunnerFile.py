from fastapi import FastAPI
import numpy as np
import tensorflow as tf
import joblib
import joblib  # for classic models

# Load models
ferac_model = tf.keras.models.load_model("models/ferac_model.keras")
dyslexia_model = tf.keras.models.load_model("models/dyslexia_model.keras")
knowledge_model = tf.keras.models.load_model("models/knowledge_model.h5")
attention_model = joblib.load("attention_rf_model.pkl")  # RF model

app = FastAPI(title="NeuroAdaptive Backend")

@app.post("/predict-emotion")
def predict_emotion(data: list):
    arr = np.array(data, dtype=float).reshape(1, -1)
    pred = ferac_model.predict(arr)[0]
    return {"emotion_vector": pred.tolist()}

@app.post("/predict-dyslexia")
def predict_dyslexia(data: list):
    arr = np.array(data, dtype=float).reshape(1, -1)
    score = float(dyslexia_model.predict(arr)[0][0])
    return {"dyslexia_risk_score": score}

@app.post("/predict-mastery")
def predict_mastery(data: list):
    arr = np.array(data, dtype=float).reshape(1, -1)
    pred = knowledge_model.predict(arr)[0]
    return {"mastery_probability": pred.tolist()}

@app.post("/predict-attention")
def predict_attention(data: list):
    arr = np.array(data, dtype=float).reshape(1, -1)
    label = attention_model.predict(arr)[0]
    proba = attention_model.predict_proba(arr)[0].max()
    state = "Focused" if label == 1 else "Distracted"
    return {"attention_state": state, "confidence": round(float(proba), 2)}
