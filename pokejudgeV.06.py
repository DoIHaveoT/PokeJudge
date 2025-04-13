import os
import gdown
import time
import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Streamlit setup
st.set_page_config(page_title="PokeJudge v0.7", layout="centered")

# Rate limiting (max 10 requests/hour)
RATE_LIMIT = 10
RATE_WINDOW = 3600  # seconds in one hour
rate_file = "usage_log.txt"

def is_rate_limited():
    if not os.path.exists(rate_file):
        return False
    with open(rate_file, "r") as f:
        timestamps = [float(ts.strip()) for ts in f.readlines()]
    now = time.time()
    # Keep only timestamps from the last hour
    recent = [ts for ts in timestamps if now - ts < RATE_WINDOW]
    return len(recent) >= RATE_LIMIT

def log_usage():
    with open(rate_file, "a") as f:
        f.write(str(time.time()) + "\n")

# Visitor counter
def increment_counter():
    count_file = "visit_count.txt"
    if not os.path.exists(count_file):
        with open(count_file, "w") as f:
            f.write("1")
            return 1
    else:
        with open(count_file, "r+") as f:
            count = int(f.read()) + 1
            f.seek(0)
            f.write(str(count))
            f.truncate()
            return count

visit_number = increment_counter()

# Download model from Google Drive if not already present
model_path = "pokejudge_v07_final.h5"
if not os.path.exists(model_path):
    file_id = "17ezhtpI4xrGSkQTWzLN6xpKnIfYAZJVe"
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    gdown.download(url, model_path, quiet=False)

# Load model
model = load_model(model_path)

# Class mapping
index_to_label = {
    0: '10',
    1: '7',
    2: '7.5',
    3: '8',
    4: '8.5',
    5: '9',
    6: '9.5'
}

# Sidebar info
with open("visit_count.txt", "r") as f:
    count = f.read()
    st.sidebar.markdown(f"👀 Visitors: **{count}**")
    st.sidebar.markdown(f"🧠 Model: pokejudge_v07_final.h5")

# Main UI
st.title("PokeJudge v0.7")
st.subheader("Upload a Pokémon card image to get an AI-generated grade")

if is_rate_limited():
    st.error("🚫 Rate limit reached! Please wait an hour before submitting more cards.")
else:
    uploaded_file = st.file_uploader("Choose a card image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        display_img = Image.open(uploaded_file)
        st.image(display_img, caption="Uploaded Card", width=350)

        model_img = image.load_img(uploaded_file, target_size=(224, 224))
        img_array = image.img_to_array(model_img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        pred = model.predict(img_array)
        predicted_class = int(np.argmax(pred))
        confidence = float(np.max(pred)) * 100
        grade = index_to_label.get(predicted_class, "Unknown")

        log_usage()

        st.markdown(f"### 🧠 Predicted Grade: **{grade}**")
        st.markdown(f"#### Confidence: {confidence:.2f}%")
