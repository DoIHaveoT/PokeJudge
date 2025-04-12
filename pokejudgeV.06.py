import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load model
model = load_model("pokejudge_v06_final.h5")

# Label mapping (based on training class indices)
index_to_label = {
    0: '10',
    1: '7',
    2: '7.5',
    3: '8',
    4: '8.5',
    5: '9',
    6: '9.5'
}

import os
import gdown

model_path = "pokejudge_v06_final.h5"
if not os.path.exists(model_path):
    file_id = "1pIuP9XBlYIQ7HS50H6WoGJxnMKPbpgSx"
    gdown.download(f"https://drive.google.com/uc?id={file_id}", model_path, quiet=False)


st.set_page_config(page_title="PokeJudge v0.6", layout="centered")
st.title("PokeJudge v0.6")
st.subheader("Upload a Pokémon card image to get an AI-generated grade")

uploaded_file = st.file_uploader("Choose a card image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = image.load_img(uploaded_file, target_size=(224, 224))
    st.image(img, caption="Uploaded Card", use_column_width=True)

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    pred = model.predict(img_array)
    predicted_class = int(np.argmax(pred))
    confidence = float(np.max(pred)) * 100

    grade = index_to_label.get(predicted_class, "Unknown")

    st.markdown(f"### 🧠 Predicted Grade: **{grade}**")
    st.markdown(f"#### Confidence: {confidence:.2f}%")
