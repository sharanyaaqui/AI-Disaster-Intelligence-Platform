import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image


from ai_model.config import MODEL_PATH, IMAGE_SIZE, CLASS_NAMES
from ai_model.recommendations import recommendations


# Load model only once
model = tf.keras.models.load_model(MODEL_PATH)


def predict_disaster(image_path, reported_disaster=None):

    # Road Damage is not currently part of the trained AI model.
    # Handle it using the report's selected disaster type.

    if reported_disaster:

        normalized_type = reported_disaster.strip().lower()

    # Map frontend incident names to recommendation names
    incident_map = {

        "fire": "wildfire",

        "wildfire": "wildfire",

        "road damage": "road damage",

        "landslide": "landslide",

        "building collapse": "building collapse",

        "other": "other"

    }

    recommendation_key = incident_map.get(
        normalized_type
    )


    # These incidents are NOT currently
    # trained classes in the AI model.
    if recommendation_key:

        recommendation = recommendations[
            recommendation_key
        ]

        return {

            "prediction": reported_disaster,

            "confidence": None,

            "severity":
                recommendation["severity"],

            "risk":
                recommendation["risk"],

            "emergency_level":
                recommendation["emergency_level"],

            "response_time":
                recommendation["response_time"],

            "actions":
                recommendation["actions"]

        }  

    # -----------------------------
    # Existing AI prediction
    # -----------------------------

    img = image.load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    img = image.img_to_array(img)

    img = np.expand_dims(img, axis=0)

    img = img / 255.0

    prediction = model.predict(
        img,
        verbose=0
    )

    class_index = np.argmax(prediction)

    confidence = float(
        np.max(prediction) * 100
    )

    disaster = CLASS_NAMES[class_index]

    recommendation = recommendations[disaster]

    return {

        "prediction": disaster,

        "confidence": round(
            confidence,
            2
        ),

        "severity":
            recommendation["severity"],

        "risk":
            recommendation["risk"],

        "emergency_level":
            recommendation["emergency_level"],

        "response_time":
            recommendation["response_time"],

        "actions":
            recommendation["actions"]

    }


# Testing
if __name__ == "__main__":

    result = predict_disaster("ai_model/test_images/sample.jpg")

    print(result)