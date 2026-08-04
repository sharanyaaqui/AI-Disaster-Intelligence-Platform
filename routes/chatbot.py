from flask import Blueprint, request, jsonify

chatbot = Blueprint("chatbot", __name__)


@chatbot.route("/predict", methods=["POST"])
def predict_disaster():

    data = request.get_json()

    description = data.get("description", "")

    description = description.lower()

    if "flood" in description:
        prediction = "Flood"

    elif "fire" in description:
        prediction = "Fire"

    elif "earthquake" in description:
        prediction = "Earthquake"

    elif "landslide" in description:
        prediction = "Landslide"

    else:
        prediction = "Unknown"

    return jsonify({
        "success": True,
        "prediction": prediction
    }), 200