import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os
from sklearn.utils.class_weight import compute_class_weight

DATA_DIR = r"D:\Micro Imagine cup\NeuroAdaptive\data\dyslexia_handwriting\raw"
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 25
MODEL_SAVE_PATH = r"D:\Micro Imagine cup\NeuroAdaptive\dyslexia_handwriting_cnn.h5"

if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Dataset directory not found: {DATA_DIR}")

train_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary"
)

val_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary"
)

class_names = train_ds.class_names
print("Class names:", class_names)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

data_augmentation = keras.Sequential([
    layers.RandomRotation(0.03),
    layers.RandomZoom(0.1),
    layers.RandomContrast(0.1),
])

model = keras.Sequential([
    layers.Rescaling(1./255, input_shape=(128, 128, 3)),
    data_augmentation,

    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(64, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.2),  # reduced dropout for confidence

    layers.Dense(1, activation="sigmoid")  # binary classifier
])

from sklearn.utils.class_weight import compute_class_weight
import numpy as np

labels = np.concatenate([y.numpy().astype(int) for _, y in train_ds])

from sklearn.utils.class_weight import compute_class_weight
import numpy as np

labels = np.concatenate([y.numpy() for _, y in train_ds])
labels = labels.astype(int).ravel()  # 🔑 THIS FIXES THE ERROR

print("Positive ratio:", labels.mean())

class_weights_values = compute_class_weight(
    class_weight="balanced",
    classes=np.array([0, 1]),
    y=labels
)

class_weight = {
    0: class_weights_values[0],
    1: class_weights_values[1]
}

print("Class weights:", class_weight)

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        keras.metrics.AUC(name="auc")
    ]
)

model.summary()

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    class_weight=class_weight
)

model.save(MODEL_SAVE_PATH)
print(f"\n✅ Model saved successfully as: {MODEL_SAVE_PATH}")
