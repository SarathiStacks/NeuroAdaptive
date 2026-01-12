import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
import pickle
import os

# =========================
# CONFIG
# =========================
DATA_PATH = r"G:\NeuroAdaptive\data\hyperaktiv\hyperaktiv_core_features.csv"
MODEL_SAVE_PATH = r"G:\NeuroAdaptive\models\attention_rf_model.pkl"
RANDOM_STATE = 42

os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(DATA_PATH)
print("Dataset loaded:", df.shape)

print("\nType column distribution:")
print(df["Type"].value_counts())

# =========================
# LABEL ENCODING
# Type = 6.0 → ADHD (1)
# Type = 0.0 → Control (0)
# =========================
df["label"] = df["Type"].apply(lambda x: 1 if x == 6.0 else 0)

print("\nLabel distribution:")
print(df["label"].value_counts())

# =========================
# FEATURE SELECTION
# =========================
DROP_COLS = [
    "ID",
    "SEX",
    "AGE",
    "Type",
    "Assessment Status",
    "label"
]

X = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
y = df["label"]

print("\nFeature matrix shape:", X.shape)

# =========================
# TRAIN / VALIDATION SPLIT
# =========================
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=RANDOM_STATE
)

# =========================
# SIMPLIFIED MODEL
# (anti-overfitting)
# =========================
model = RandomForestClassifier(
    n_estimators=50,
    max_depth=3,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=RANDOM_STATE
)

print("\nTraining Random Forest model...")
model.fit(X_train, y_train)

# =========================
# HOLD-OUT EVALUATION
# =========================
pred = model.predict(X_val)
bal_acc = balanced_accuracy_score(y_val, pred)
print("\nBalanced Accuracy (Hold-out):", round(bal_acc, 4))

# =========================
# LEAVE-ONE-MINORITY-OUT CV
# =========================
minority_idx = y[y == 0].index.tolist()
minority_cv_scores = []

for idx in minority_idx:
    X_train_cv = X.drop(index=idx)
    y_train_cv = y.drop(index=idx)

    X_test_cv = X.loc[[idx]]
    y_test_cv = y.loc[[idx]]

    model_cv = RandomForestClassifier(
        n_estimators=50,
        max_depth=3,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_STATE
    )

    model_cv.fit(X_train_cv, y_train_cv)
    pred_cv = model_cv.predict(X_test_cv)

    minority_cv_scores.append(int(pred_cv[0] == y_test_cv.iloc[0]))

minority_cv_scores = np.array(minority_cv_scores)

print("\nLeave-One-Minority-Out CV results:")
print(minority_cv_scores)
print("Mean Minority CV Accuracy:", round(minority_cv_scores.mean(), 4))

# =========================
# SAVE MODEL
# =========================
with open(MODEL_SAVE_PATH, "wb") as f:
    pickle.dump(model, f)

print("\nModel saved at:", MODEL_SAVE_PATH)

# =========================
# SYSTEM-READY INFERENCE DEMO
# =========================
sample = X_val.iloc[0].to_frame().T
probs = model.predict_proba(sample)[0]

attention_state = "distracted" if probs[1] >= 0.5 else "focused"
confidence = round(abs(probs[1] - 0.5) * 2, 4)

print("\nExample output for system integration:")
print({
    "attention_state": attention_state,
    "confidence": confidence
})
