import streamlit as st
import requests

st.set_page_config(page_title="Smart Packaging Predictor", layout="centered")

st.title("📦 Precise Packaging Predictor")
st.markdown("Enter product details to get packaging recommendations.")

# Input fields
weight = st.number_input("Weight (kg)", min_value=0.0)
length = st.number_input("Length (cm)", min_value=0.0)
width = st.number_input("Width (cm)", min_value=0.0)
height = st.number_input("Height (cm)", min_value=0.0)


# API URL
api_url = "https://precise-packing-method.onrender.com/predict"
# ✅ Check API Status with a test POST request
try:
    test_payload = {"weight": 1.0, "length": 1.0, "width": 1.0, "height": 1.0}
    response = requests.post(api_url, json=test_payload)

    if response.status_code == 200:
        st.success("✅ API is running!")
    else:
        st.error(f"🚨 API error: {response.text}")
except requests.exceptions.RequestException:
    st.error("⚠ API is unreachable. Check internet or server status.")

if st.button("🔍 Predict Packaging Material"):
    if weight and length and width and height:
        payload = {
            "weight": weight,
            "length": length,
            "width": width,
            "height": height,
           
            
        }

        with st.spinner("Predicting..."):
            response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            prediction = response.json().get("prediction", "Error")
            st.success(f"🧠 Recommended Packaging: **{prediction}**")
        else:
            st.error("❌ API Error. Please check inputs or server.")
    else:
        st.warning("Please fill all input fields.")
