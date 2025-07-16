from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io
import os
import subprocess

app = Flask(__name__)

MODEL_PATH = "artifacts/training/model.keras"
S3_URI = "s3://ct-kideny-data/model/model.keras"
if not os.path.exists(MODEL_PATH):
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    subprocess.run(["aws", "s3", "cp", S3_URI, MODEL_PATH], check=True)
model = load_model(MODEL_PATH)
class_labels = ["Cyst", "Normal", "Stone", "Tumor"]

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        img = Image.open(io.BytesIO(file.read())).convert("RGB")
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        preds = model.predict(img_array)
        predicted_class = class_labels[np.argmax(preds)]

        return jsonify({
            "prediction": predicted_class,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
