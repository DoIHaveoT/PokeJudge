
import os
import gdown
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


st.set_page_config(page_title="PokeJudge v0.7", layout="centered")
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
    file_id = "17ezhtpI4xrGSkQTWzLN6xpKnIfYAZJVe"  # your actual file ID
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    gdown.download(url, model_path, quiet=False)

# Load the model after it’s downloaded
model = load_model(model_path)

# Label mapping (based on your training folder order)
index_to_label = {
    0: '10',
    1: '7',
    2: '7.5',
    3: '8',
    4: '8.5',
    5: '9',
    6: '9.5'
}

# Streamlit UI
# Display visitor count in the sidebar
with open("visit_count.txt", "r") as f:
    count = f.read()
    st.sidebar.markdown(f"👀 Visitors: **{count}**")

st.title("PokeJudge v0.7")
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
=======
import os
import gdown
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


st.set_page_config(page_title="PokeJudge v0.7", layout="centered")
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
    file_id = "17ezhtpI4xrGSkQTWzLN6xpKnIfYAZJVe"  # your actual file ID
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    gdown.download(url, model_path, quiet=False)

# Load the model after it’s downloaded
model = load_model(model_path)

# Label mapping (based on your training folder order)
index_to_label = {
    0: '10',
    1: '7',
    2: '7.5',
    3: '8',
    4: '8.5',
    5: '9',
    6: '9.5'
}

# Streamlit UI
st.markdown(f"👥 You are visitor **#{visit_number}**")

st.title("PokeJudge v0.7")
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
>>>>>>> 9683d231f5203285934503974c930f90748f7a40
