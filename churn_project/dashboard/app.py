import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

# =========================
# Header
# =========================
st.title("📊 Customer Churn Prediction Dashboard")
st.caption("AI-based Decision Support System for Telecom Retention Teams")

st.markdown("---")

# =========================
# Input Section
# =========================
st.subheader("Customer Information")

col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", ["Yes", "No"])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])

with col2:
    tenure = st.number_input("Tenure Months", min_value=0)
    monthly = st.number_input("Monthly Charges", min_value=0.0)
    total = st.number_input("Total Charges", min_value=0.0)
    cltv = st.number_input("CLTV", min_value=0.0)

with col3:
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    payment = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Credit card (automatic)",
            "Bank transfer (automatic)"
        ]
    )
    latitude = st.number_input("Latitude", value=34.0)
    longitude = st.number_input("Longitude", value=-118.0)

st.markdown("---")

# =========================
# Prediction Button
# =========================
if st.button("🔍 Predict Churn Risk"):

    payload = {
        "Gender": gender,
        "Senior_Citizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "Tenure_Months": tenure,
        "Contract": contract,
        "Phone_Service": "Yes",
        "Multiple_Lines": "No",
        "Internet_Service": "Fiber optic",
        "Online_Security": "No",
        "Online_Backup": "No",
        "Device_Protection": "No",
        "Tech_Support": "No",
        "Streaming_TV": "No",
        "Streaming_Movies": "No",
        "Paperless_Billing": "Yes",
        "Payment_Method": payment,
        "Monthly_Charges": monthly,
        "Total_Charges": total,
        "CLTV": cltv,
        "Latitude": latitude,
        "Longitude": longitude
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=payload)

    if response.status_code == 200:
        res = response.json()
        prob = res["churn_probability"]

        # =========================
        # KPI Cards
        # =========================
        st.subheader("Prediction Results")

        k1, k2, k3 = st.columns(3)

        k1.metric("Churn Probability", f"{prob*100:.1f}%")

        prediction_label = "Churn" if res["prediction"] == 1 else "No Churn"
        k2.metric("Prediction", prediction_label)

        if prob >= 0.7:
            risk = "High Risk"
        elif prob >= 0.4:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        k3.metric("Risk Level", risk)

        st.markdown("---")

        # =========================
        # Churn Risk Visualization
        # =========================
        st.subheader("Churn Risk Indicator")

        prob_df = pd.DataFrame(
            {"Risk": ["Churn Probability"], "Value": [prob]}
        ).set_index("Risk")

        st.bar_chart(prob_df)

        st.markdown("---")

        # =========================
        # Business Insight
        # =========================
        st.subheader("Customer Insight")

        if res["prediction"] == 1:
            st.warning(
                "This customer shows a **high likelihood of churn**. "
                "Recommended actions include offering retention incentives, "
                "discounts, or contract upgrades."
            )
        else:
            st.success(
                "This customer shows a **low churn risk**. "
                "Current engagement strategy appears effective."
            )

    else:
        st.error("Prediction failed")
        st.json(response.json())
