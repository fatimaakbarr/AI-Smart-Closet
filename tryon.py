import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import os
import io
from rembg import remove

st.set_page_config(page_title="AI Smart Closet", layout="wide")
st.title("👕 AI Smart Closet")

# --- 1. Setup Folders ---
os.makedirs("shirts", exist_ok=True)
os.makedirs("people", exist_ok=True)

# --- 2. AI Memory Banks (The Fix!) ---
# These @st.cache decorators stop the app from re-running the heavy AI every time you touch a slider.
@st.cache_resource
def load_pose_model():
    return mp.solutions.pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

pose = load_pose_model()

@st.cache_data
def get_clean_shirt(image_path):
    with st.spinner("AI is extracting the shirt..."):
        img = Image.open(image_path).convert("RGBA")
        clean_img = remove(img)
        bbox = clean_img.getbbox()
        if bbox:
            return clean_img.crop(bbox)
        return clean_img

@st.cache_data
def analyze_person(image_path):
    with st.spinner("AI is measuring shoulders..."):
        img = Image.open(image_path).convert("RGBA")
        rgb = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2RGB)
        results = pose.process(rgb)
        return img, results

# --- 3. Sidebar Controls ---
with st.sidebar:
    st.header("1. Your Photo")
    person_file = st.file_uploader("Upload your photo", type=["jpg", "png", "jpeg"])
    if person_file:
        path = os.path.join("people", person_file.name)
        with open(path, "wb") as f:
            f.write(person_file.getbuffer())
        st.session_state['person_path'] = path

    st.header("2. Add to Collection")
    custom_shirt = st.file_uploader("Upload any shirt", type=["jpg", "png", "jpeg"])
    if custom_shirt:
        path = os.path.join("shirts", custom_shirt.name)
        with open(path, "wb") as f:
            f.write(custom_shirt.getbuffer())
        st.session_state['active_shirt'] = path
        st.success("Added!")

    st.header("3. Tailor Fit")
    # The scale slider you wanted, now instant!
    shirt_scale = st.slider("Scale Size", min_value=1.0, max_value=4.0, value=2.2, step=0.1)
    # A new slider to pull the collar up or push it down
    y_offset = st.slider("Collar Height (Up/Down)", min_value=-150, max_value=150, value=0, step=5)

# --- 4. Dynamic Gallery ---
st.subheader("Your Collection")
shirt_files = [f for f in os.listdir("shirts") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if shirt_files:
    cols = st.columns(min(len(shirt_files), 6)) # Show up to 6 shirts
    for i, shirt_name in enumerate(shirt_files[:6]):
        path = os.path.join("shirts", shirt_name)
        cols[i].image(Image.open(path), width=80)
        if cols[i].button("Wear", key=f"wear_{i}"):
            st.session_state['active_shirt'] = path

# --- 5. The Try-On Engine ---
if 'person_path' in st.session_state and 'active_shirt' in st.session_state:
    
    # Load from our fast memory banks
    person_img, pose_results = analyze_person(st.session_state['person_path'])
    shirt_img = get_clean_shirt(st.session_state['active_shirt'])

    if pose_results.pose_landmarks:
        landmarks = pose_results.pose_landmarks.landmark
        w, h = person_img.size
        
        # Shoulders
        l_s = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        r_s = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        lx, ly = int(l_s.x * w), int(l_s.y * h)
        rx, ry = int(r_s.x * w), int(r_s.y * h)
        
        # Math
        shoulder_width = abs(lx - rx)
        mid_x = (lx + rx) // 2
        mid_y = (ly + ry) // 2
        
        # Scaling (Controlled by your slider)
        orig_w, orig_h = shirt_img.size
        new_w = int(shoulder_width * shirt_scale)
        new_h = int(orig_h * (new_w / orig_w))
        resized_shirt = shirt_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Anchor (Controlled by the math + your offset slider)
        paste_x = mid_x - (new_w // 2)
        paste_y = (mid_y - int(shoulder_width * 0.3)) + y_offset
        
        # Paste
        result_img = Image.new("RGBA", person_img.size)
        result_img = Image.alpha_composite(result_img, person_img)
        result_img.paste(resized_shirt, (paste_x, paste_y), resized_shirt)
        
        st.image(result_img.convert("RGB"), caption="Your Tailored Fit", use_container_width=True)
    else:
        st.error("AI couldn't find your shoulders!")
else:
    st.info("👈 Upload your photo and pick a shirt to begin!")