import tensorflow as tf

from preprocessing import train_data, validation_data
from model import model
from config import *

# Compile Model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Callbacks
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    MODEL_PATH,
    monitor="val_accuracy",
    save_best_only=True
)

# Train Model
history = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=EPOCHS,
    callbacks=[early_stop, checkpoint]
)

import pickle

with open("ai_model/history.pkl", "wb") as f:
    pickle.dump(history.history, f)


print("\nTraining Completed Successfully!")

model.save(MODEL_PATH)

# import os

# os.makedirs("ai_model/models", exist_ok=True)

# model.save("ai_model/models/disaster_classifier.keras")

# print("Model Saved Successfully!")