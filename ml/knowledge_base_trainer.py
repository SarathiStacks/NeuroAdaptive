import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
import pickle

# Load datasets
Xq = np.load(r"D:\Micro Imagine cup\NeuroAdaptive\data\ednet\X_questions.npy")
Xa = np.load(r"D:\Micro Imagine cup\NeuroAdaptive\data\ednet\X_answers.npy")

# Extract correctness signal (0 = wrong, 1 = correct)
correctness = (Xa > 0).astype(np.float32)

# Prepare input for LSTM (students, timesteps, 1 feature)
X = correctness.reshape(correctness.shape[0], correctness.shape[1], 1)

# Label = last timestep correctness (what the model will predict mastery from)
y = correctness[:, -1]

# Split train/val
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

print("Train shape:", X_train.shape, "Val shape:", X_val.shape)
print("Label distribution:", np.unique(y, return_counts=True))

# Build LSTM model
model = models.Sequential([
    layers.Input(shape=(X_train.shape[1], 1)),
    layers.LSTM(64, return_sequences=False),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Train
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=15,
    batch_size=8
)

# Save model
model.save("knowledge_tracing_lstm.h5")

# Save model backup as pickle
with open("knowledge_tracing_lstm.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel saved as: knowledge_tracing_lstm.h5 and knowledge_tracing_lstm.pkl")

# Test inference output format
sample = X_val[0].reshape(1, X_val.shape[1], 1)
score = model.predict(sample)[0][0]

print("\nIntegration-ready output example:")
print({ "concept_mastery": float(round(score, 4)), "confidence": float(round(score, 4)) })
