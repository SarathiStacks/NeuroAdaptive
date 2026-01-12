import numpy as np
from tensorflow import keras

MODEL_PATH = r"D:\Micro Imagine cup\NeuroAdaptive\backend\models\dyslexia_handwriting_cnn.h5"

kt_model = keras.models.load_model(MODEL_PATH, compile=False)

def predict_mastery(correctness_sequence):
    """
    correctness_sequence: list of 0/1 values
    Returns mastery score between 0 and 1
    """

    arr = np.array(correctness_sequence, dtype=np.float32)
    arr = arr.reshape(1, arr.shape[0], 1)

    mastery = float(kt_model.predict(arr, verbose=0)[0][0])
    return mastery
