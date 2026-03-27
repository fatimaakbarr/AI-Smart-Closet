# 👕 AI Smart Closet

A Python-based virtual try-on web application built with Streamlit. This app uses computer vision and AI to automatically measure a person's shoulders and scale digital clothing to perfectly fit their body.

## ✨ Features
* **AI Pose Detection:** Uses Google's `MediaPipe` to find the user's shoulders and calculate real-time body proportions.
* **Smart Background Removal:** Uses `rembg` to automatically cut out t-shirts from any uploaded image.
* **Dynamic Tailoring:** Automatically scales the clothing to match the user's shoulder width (with manual slider overrides for the perfect fit).
* **Interactive Web UI:** Built entirely in `Streamlit` for a fast, browser-based experience.

## 🚀 How to Run Locally

1. Clone this repository:
   ```bash
   git clone [https://github.com/fatimaakbarr/AI-Smart-Closet.git](https://github.com/fatimaakbarr/AI-Smart-Closet.git)
   cd AI-Smart-Closet
Install the required AI libraries:

Bash
pip install -r requirements.txt
Launch the web app:

Bash
streamlit run tryon.py
🛠️ Built With
Streamlit - The web framework

MediaPipe - AI Pose Estimation

OpenCV - Image processing

Rembg - Background removal