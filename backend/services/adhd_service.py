import numpy as np
import joblib
from tensorflow import keras

MODEL_PATH = r"D:\Micro Imagine cup\NeuroAdaptive\backend\models\attention_rf_model.pkl"

attention_model = joblib.load(MODEL_PATH)

def get_attention_feedback(
    time_taken: list[float],
    correctness: list[int]
) -> tuple[float, str]:
    """
    Predicts attention score using a RandomForest ADHD model.

    Inputs:
    - time_taken: list of time spent per question
    - correctness: list of 0/1 values

    Returns:
    - attention_score (0–1)
    - attention_feedback (string)
    """

    if not time_taken or not correctness:
        return 0.0, "Not enough data to assess attention."
    avg_time = float(np.mean(time_taken))
    std_time = float(np.std(time_taken))
    accuracy = float(np.mean(correctness))
    hesitation = float(np.mean([1 if t > avg_time else 0 for t in time_taken]))
    features = np.zeros(794, dtype=np.float32)
    features[0] = avg_time
    features[1] = std_time
    features[2] = accuracy
    features[3] = hesitation

    X = features.reshape(1, -1)
    proba = attention_model.predict_proba(X)[0]
    attention_score = float(proba[1])  # probability of "high attention"

    if attention_score > 0.6:
        msg = "Your attention level is high — great focus! 🎯"
    elif attention_score > 0.3:
        msg = "You’re doing okay, try to stay a little more engaged."
    else:
        msg = "Attention seems low. A short break might help 💛"

    return attention_score, msg