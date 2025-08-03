import cv2
import numpy as np
import streamlit as st
# Existing model for image classification
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from PIL import Image

def load_model():
    """Load the pre-trained MobileNetV2 model."""
    model = MobileNetV2(weights='imagenet')
    return model

def preprocess_image(image):
    """Preprocess the image for the model."""
    img = np.array(image)
    img = cv2.resize(img, (224, 224))  # Resize to model input size
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img


def classify_image(model, image):
    """Classify the image using the pre-trained model."""
    try:
        processed_image = preprocess_image(image) # Preprocess the image
        predictions = model.predict(processed_image) # Predict the image identity and return a percentage
        decoded_predictions = decode_predictions(predictions, top=3)[0] # Take top 3 predictions
        return decoded_predictions
    except Exception as e:
        st.error(f"Error classifying image: {str(e)}")
        return None
    
def main():
    st.set_page_config(page_title="AI Image Classifier", page_icon=":camera:", layout="centered")
    st.title("AI Image Classifier")
    st.write("Upload an image to classify it using a pre-trained model.")

    # Cache the model to avoid reloading it on every run.
    @st.cache_resource
    def load_cached_model():
        return load_model()
    
    model = load_cached_model()
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True,
        )
        btn = st.button("Classify Image")

        if btn:
            with st.spinner("Analyzing Image..."):
                image = Image.open(uploaded_file)
                predictions = classify_image(model, image)

                if predictions:
                    st.subheader("Predictions:")
                    # (0, "car", 0.95) -> (label, score) first value irrelevant
                    for _, label, score in predictions:
                        st.write(f"**{label}**: {score:.2%}")


if __name__ == "__main__":
    main()