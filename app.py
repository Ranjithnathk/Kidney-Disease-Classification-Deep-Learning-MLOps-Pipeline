import streamlit as st
import requests
from PIL import Image
import io

# Backend Flask API endpoint
API_URL = "http://3.144.116.189:8080/predict"

# Title
st.title("Kidney Disease Classification")
st.write("Upload a kidney CT image and get the prediction from the model.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display image preview (smaller)
    st.image(uploaded_file, caption="Uploaded Image", width=250)

    if st.button("Predict"):
        # Call Flask API
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(API_URL, files={"file": io.BytesIO(files["file"])})

        if response.status_code == 200:
            result = response.json()
            st.success(f"Prediction: **{result['prediction']}**")
        else:
            st.error(f"Prediction failed: {response.json().get('error', 'Unknown error')}")
