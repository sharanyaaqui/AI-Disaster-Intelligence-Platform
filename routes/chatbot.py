from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

from ai_model.predict import predict_disaster

chatbot = Blueprint("chatbot", __name__)

UPLOAD_FOLDER = "uploads"


@chatbot.route("/predict", methods=["POST"])
def predict():

    print("========== PREDICT API CALLED ==========")

    # Check image exists
    if "image" not in request.files:
        print("ERROR: No image in request")
        return jsonify({
            "success": False,
            "message": "No image uploaded"
        }), 400

    image = request.files["image"]

    print("Image received:", image.filename)

    # Check filename
    if image.filename == "":
        print("ERROR: Empty filename")
        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    # Create upload folder
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(image.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save image
    image.save(filepath)

    print("IMAGE SAVED:", filepath)

    # Run AI prediction
    print("STARTING AI PREDICTION...")

    result = predict_disaster(filepath)

    print("PREDICTION DONE:")
    print(result)

    return jsonify({
        "success": True,
        "result": result
    }), 200