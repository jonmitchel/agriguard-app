
import streamlit as st
import pandas as pd

# Title
st.title("AgriGuard: Pest and Disease Risk Forecaster")

# Description
st.write("""
This app predicts the risk level of pest or disease outbreaks based on environmental conditions and crop stage.
Provide the required inputs below to get the forecast.
""")

# Forecast logic
def forecast_pest(temp, humidity, rainfall, crop_stage):
    risk_score = 0
    if temp > 30:
        risk_score += 1
    if humidity > 80:
        risk_score += 1
    if rainfall > 30:
        risk_score += 1
    if crop_stage == "Flowering":
        risk_score += 1

    if risk_score >= 3:
        return "High Risk"
    elif risk_score == 2:
        return "Medium Risk"
    else:
        return "Low Risk"

# Manual input section
st.markdown("### 🧪 Manual Forecast Input")

col1, col2 = st.columns(2)

with col1:
    temp = st.number_input("🌡️ Temperature (°C)", min_value=10, max_value=50, value=30)
    rainfall = st.number_input("🌧️ Rainfall (mm)", min_value=0, max_value=200, value=40)

with col2:
    humidity = st.number_input("💧 Humidity (%)", min_value=10, max_value=100, value=80)
    crop_stage = st.selectbox("🌱 Crop Stage", ["Vegetative", "Flowering", "Fruiting"])

if st.button("📊 Forecast Risk"):
    risk_level = forecast_pest(temp, humidity, rainfall, crop_stage)
    st.subheader(f"🩺 Predicted Risk Level: **{risk_level}**")

    # Color-coded message
    if risk_level == "High Risk":
        st.error("🚨 Immediate action required: High chance of pest or disease outbreak.")
    elif risk_level == "Medium Risk":
        st.warning("⚠️ Monitor closely: Conditions moderately favor outbreaks.")
    else:
        st.success("✅ Low risk: Conditions are currently stable.")

# File upload section
st.markdown("---")
st.subheader("📁 Upload CSV for Batch Forecasting")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df_input = pd.read_csv(uploaded_file)

    def forecast_row(row):
        return forecast_pest(
            row["Temperature (°C)"],
            row["Humidity (%)"],
            row["Rainfall (mm)"],
            row["Crop Stage"]
        )

    df_input["Risk Level"] = df_input.apply(forecast_row, axis=1)
    st.write("### 📋 Forecast Results")
    st.dataframe(df_input)

    csv_output = df_input.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv_output,
        file_name="AgriGuard_Forecast_Results.csv",
        mime="text/csv"
    )
