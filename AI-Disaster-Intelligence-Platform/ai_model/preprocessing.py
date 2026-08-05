import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from config import *

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(
    rescale=1./255
)

validation_datagen = ImageDataGenerator(
    rescale=1./255
)

train_data = train_datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

test_data = test_datagen.flow_from_directory(
    TEST_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

validation_data = validation_datagen.flow_from_directory(
    VALIDATION_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

print("\n================================")
print("Dataset Loaded Successfully!")
print("================================")
print(f"Training Images   : {train_data.samples}")
print(f"Testing Images    : {test_data.samples}")
print(f"Validation Images : {validation_data.samples}")
print(f"Classes           : {train_data.class_indices}")