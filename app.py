import os
from typing import Tuple

import numpy as np
from flask import Flask, jsonify, request
from PIL import Image, UnidentifiedImageError

try:
    import tensorflow as tf
except Exception as e:  # pragma: no cover
    raise RuntimeError(
        "Failed to import TensorFlow. Ensure it is installed per requirements.txt"
    ) from e


# Configuration
MODEL_PATH = os.getenv("MODEL_PATH", "ResNet50V2_Model.h5")
EMOTION_CLASSES = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise",
]
TARGET_SIZE: Tuple[int, int] = (224, 224)


def _load_model(path: str):
    """Load and return the Keras model once at startup."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file not found at '{path}'. Set MODEL_PATH env var or place the file there."
        )
    model = tf.keras.models.load_model(path)
    return model


model = _load_model(MODEL_PATH)


def preprocess_image(file_obj) -> np.ndarray:
    """Preprocess the uploaded image to match model input.

    Steps:
    - Convert to RGB
    - Resize to 224x224
    - Normalize by 255.0
    - Add batch dimension
    """
    img = Image.open(file_obj).convert("RGB")
    img = img.resize(TARGET_SIZE)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr


def predict_emotion(arr: np.ndarray) -> Tuple[str, float]:
    """Run prediction and return (label, confidence)."""
    preds = model.predict(arr)
    probs = preds[0]
    idx = int(np.argmax(probs))
    label = EMOTION_CLASSES[idx]
    confidence = float(probs[idx])
    return label, confidence


app = Flask(__name__)


@app.route("/health", methods=["GET"])  # Optional helper endpoint
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": bool(model),
        "model_path": MODEL_PATH,
        "classes": EMOTION_CLASSES,
    })


@app.route("/predict", methods=["POST"])
def predict():
    # Validate file presence (accept either 'file' or 'image' as key)
    if "file" not in request.files and "image" not in request.files:
        return (
            jsonify({"error": "No image file provided. Use form key 'file' or 'image'."}),
            400,
        )

    file = request.files.get("file") or request.files.get("image")
    if not file or file.filename == "":
        return jsonify({"error": "Empty filename or no file uploaded."}), 400

    try:
        arr = preprocess_image(file.stream)
    except UnidentifiedImageError:
        return jsonify({"error": "Uploaded file is not a valid image."}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 400

    try:
        label, confidence = predict_emotion(arr)
    except Exception as e:  # Model or inference issues
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    return jsonify({"emotion": label, "confidence": round(confidence, 4)})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
