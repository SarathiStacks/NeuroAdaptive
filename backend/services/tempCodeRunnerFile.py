import numpy as np
from tensorflow import keras

MODEL_PATH = r"D:\Micro Imagine cup\NeuroAdaptive\backend\models\knowledge_tracing_lstm.h5"

KT_MODEL = keras.models.load_model(MODEL_PATH, compile=False)

def predict_knowledge(series: list) -> float:
    """Returns topic mastery score from knowledge tracing model"""
    arr = np.array(series, dtype=np.float32).reshape(1, -1, 1)
    return float(KT_MODEL.predict(arr, verbose=0)[0][0])
