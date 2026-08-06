import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

from config import *
from config import MODEL_PATH, IMAGE_SIZE, CLASS_NAMES
from recommendations import recommendations

# Load model only once
model = tf.keras.models.load_model(MODEL_PATH)


def predict_disaster(image_path):

    img = image.load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    img = image.img_to_array(img)

    img = np.expand_dims(img, axis=0)

    img = img / 255.0

    prediction = model.predict(img, verbose=0)

    class_index = np.argmax(prediction)

    confidence = float(np.max(prediction) * 100)

    disaster = CLASS_NAMES[class_index]

    return {

       "prediction": disaster,

    "confidence": round(confidence,2),

    "severity": recommendations[disaster]["severity"],

    "risk": recommendations[disaster]["risk"],

    "emergency_level": recommendations[disaster]["emergency_level"],

    "response_time": recommendations[disaster]["response_time"],

    "actions": recommendations[disaster]["actions"]

}


# Testing
if __name__ == "__main__":

    result = predict_disaster("ai_model/test_images/sample.jpg")

    print(result)