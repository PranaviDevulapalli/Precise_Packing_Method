import streamlit as st
import requests
import pandas as pd
import hashlib
import time

# Session State for storing predictions
if "predictions" not in st.session_state:
    st.session_state.predictions = []

st.set_page_config(page_title="Smart Packaging Predictor", layout="centered")

st.title("📦 Precise Packaging Predictor")
st.markdown("Enter product details to get packaging recommendations.")

# Input fields
weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
length = st.number_input("Length (cm)", min_value=0.0, step=0.1)
width = st.number_input("Width (cm)", min_value=0.0, step=0.1)
height = st.number_input("Height (cm)", min_value=0.0, step=0.1)

# API URL
api_url = "https://precise-packing-method.onrender.com/predict"

# ✅ Check API Status with a test request
try:
    test_payload = {"weight": 1.0, "length": 1.0, "width": 1.0, "height": 1.0}
    response = requests.post(api_url, json=test_payload)

    if response.status_code == 200:
        st.success("✅ API is running!")
    else:
        st.error(f"🚨 API error: {response.text}")
except requests.exceptions.RequestException:
    st.error("⚠ API is unreachable. Check internet or server status.")

# 🔍 Predict for a Single Product
if st.button("🔍 Predict Packaging Material"):
    if weight and length and width and height:
        volume = length * width * height  # ✅ Compute volume

        payload = {
            "weight": weight,
            "length": length,
            "width": width,
            "height": height,
            "volume": volume,  # ✅ Include volume
        }

        with st.spinner("Predicting..."):
            response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            prediction = response.json().get("prediction", "Error")
            st.success(f"🧠 Recommended Packaging: **{prediction}**")
        else:
            st.error(f"❌ API Error: {response.text}")
    else:
        st.warning("⚠ Please fill all input fields.")

# --- BULK PREDICTION ---
st.markdown("---")
st.subheader("📥 Bulk Prediction (Upload CSV)")

csv_file = st.file_uploader("Upload a CSV file with columns: weight, length, width, height", type=["csv"])

if csv_file is not None:
    df = pd.read_csv(csv_file)

    if all(col in df.columns for col in ["weight", "length", "width", "height"]):
        st.dataframe(df)

        if st.button("📦 Predict for All Rows", key="predict_bulk"):
            results = []
            for _, row in df.iterrows():
                payload = {
                    "weight": row["weight"],
                    "length": row["length"],
                    "width": row["width"],
                    "height": row["height"]
                }
                res = requests.post(api_url, json=payload)
                pred = res.json().get("prediction", "Error")
                results.append(pred)

            df["Predicted Material"] = results
            st.success("✅ Bulk Predictions Completed!")
            st.dataframe(df)

            # Download option
            csv_download = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Results as CSV", csv_download, file_name="packaging_predictions.csv", mime="text/csv")
    else:
        st.warning("⚠ CSV must contain columns: weight, length, width, height")

# --- VISUALIZATION ---
if st.session_state.predictions:
    st.subheader("📊 Packaging Stats (This Session)")
    pred_df = pd.DataFrame(st.session_state.predictions, columns=["Material"])
    material_counts = pred_df["Material"].value_counts()
    st.bar_chart(material_counts)

# --- BLOCKCHAIN STYLE HASH ---
def generate_hash(prediction, payload):
    data = f"{prediction}-{payload}-{time.time()}"
    return hashlib.sha256(data.encode()).hexdigest()
