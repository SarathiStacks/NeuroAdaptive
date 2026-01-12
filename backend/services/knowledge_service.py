import numpy as np
from tensorflow import keras 
import os

MODEL_PATH = r"D:\Micro Imagine cup\NeuroAdaptive\backend\models\dyslexia_handwriting_cnn.h5"

kt_model = keras.models.load_model(MODEL_PATH, compile=False)


def predict_mastery(correctness_sequence: list[float]) -> float:
    """
    Predicts learner mastery using Knowledge Tracing LSTM.

    Parameters:
    - correctness_sequence: List of 0/1 values indicating wrong/correct answers

    Returns:
    - mastery_score: float between 0 and 1
    """

    if not correctness_sequence:
        return 0.0

    # Convert to numpy array
    sequence = np.array(correctness_sequence, dtype=np.float32)

    # Shape: (batch_size=1, timesteps, features=1)
    sequence = sequence.reshape(1, -1, 1)

    # Predict mastery
    prediction = kt_model.predict(sequence, verbose=0)

    # Output is usually [[score]]
    mastery_score = float(prediction[0][0])

    # Clamp for safety
    mastery_score = max(0.0, min(1.0, mastery_score))

    return mastery_score
