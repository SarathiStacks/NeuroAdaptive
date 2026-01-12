import numpy as np

def build_attention_features(responses):
    times = [r["time_taken"] for r in responses]
    corrects = [1 if r["correct"] else 0 for r in responses]

    features = [
        np.mean(times),
        np.std(times),
        np.min(times),
        np.max(times),
        np.mean(corrects),
        sum(corrects),
        len(corrects) - sum(corrects),
        np.mean(times) * (1 - np.mean(corrects)),
    ]

    # TEMP: pad to match trained model size
    while len(features) < 794:
        features.append(0.0)

    return np.array(features).reshape(1, -1)
