import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://54.226.13.63:8000/"

# ========================
# Page Config
# ========================
st.set_page_config(
    page_title="Customer Churn Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# Custom CSS for Cards & Buttons
# ========================
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}
.card h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 400;
}
.card h2 {
    margin: 5px 0 0 0;
    font-size: 28px;
    font-weight: 700;
}
.stButton>button {
    border-radius: 10px;
    padding: 0.4em 0.8em;
    color: white;
    font-weight: 600;
    background-color: #764ba2;
}
.stButton>button:hover {
    background-color: #667eea;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ========================
# Sidebar Navigation
# ========================
st.sidebar.title("Churn Dashboard")
st.sidebar.markdown("---")

if "page" not in st.session_state:
    st.session_state.page = "Personal Prediction"

if st.sidebar.button("Personal Prediction", use_container_width=True):
    st.session_state.page = "Personal Prediction"

if st.sidebar.button("Company Analytics", use_container_width=True):
    st.session_state.page = "Company Analytics"

page = st.session_state.page

st.sidebar.markdown("---")
st.sidebar.caption("AI-powered Telecom Decision Support System")


# ========================
# Metric Card Function
# ========================
def metric_card(title, value, color="#764ba2"):
    st.markdown(f"""
    <div class="card" style="background:{color}">
        <h3>{title}</h3>
        <h2>{value}</h2>
    </div>
    """, unsafe_allow_html=True)

# ========================
# Page 1: Personalized Prediction
# ========================
if page == "Personal Prediction":
    st.title("Personalized Churn Prediction")
    st.write("Predict churn probability for a single customer.")

    with st.form("customer_form"):
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
                ["Electronic check", "Mailed check", "Credit card (automatic)", "Bank transfer (automatic)"]
            )
        submitted = st.form_submit_button("🔍 Predict Churn Risk")

    if submitted:
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
            "CLTV": cltv
        }

        res = requests.post(f"{API_URL}/predict", json=payload)
        if res.status_code == 200:
            data = res.json()
            prob = data["churn_probability"]

            # Risk Level & Color
            if prob >= 0.7: risk, color = "High", "#FF4B4B"
            elif prob >= 0.4: risk, color = "Medium", "#FFA500"
            else: risk, color = "Low", "#4BCB9B"

            st.markdown("---")
            st.subheader("Prediction Result")

            # Metric Cards (5 like Company Analytics)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1: metric_card("Churn Probability", f"{prob*100:.1f}%", color)
            with col2: metric_card("Prediction", "Churn" if data["prediction"] else "No Churn", color)
            with col3: metric_card("Risk Level", risk, color)
            with col4: metric_card("Monthly Charges", f"${monthly:.2f}", "#667eea")
            with col5: metric_card("Tenure (Months)", f"{tenure}", "#667eea")

            # Horizontal Bar Chart like Company Analytics
            # ========================
            # Vertical Bar Chart (Personal Prediction)
            # ========================
            fig = px.bar(
                x=["Churn Probability"],       # x-axis: labels
                y=[prob],                      # y-axis: value
                text=[f"{prob*100:.1f}%"],     # show text on bars
                color=["Churn Probability"],    # just for color
                color_discrete_map={"Churn Probability": color},
                labels={"x":"Metric","y":"Probability"}
            )
            fig.update_layout(
                yaxis=dict(range=[0,1]),       # y-axis from 0 to 1
                height=300,
                margin=dict(l=20,r=20,t=20,b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("Prediction failed. Check backend server.")

# ========================
# Page 2: Company Analytics
# ========================
if page == "Company Analytics":
    st.title("Company-Level Churn Analytics")

    if st.button("Load Analytics"):
        with st.spinner("Fetching analytics from backend..."):
            res = requests.get(f"{API_URL}/analytics")

        if res.status_code == 200:
            data = res.json()

            # Metric cards
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1: metric_card("Total Customers", data["total_customers"], "#667eea")
            with col2: metric_card("High Risk", data["high_risk"], "#FF4B4B")
            with col3: metric_card("Medium Risk", data["medium_risk"], "#FFA500")
            with col4: metric_card("Low Risk", data["low_risk"], "#4BCB9B")
            with col5: metric_card("Critical %", f"{data['critical_percentage']}%", "#FF4B4B")

            st.markdown("---")
            st.subheader("Risk Distribution")
            fig = px.bar(
                x=["High Risk", "Medium Risk", "Low Risk"],
                y=[data["high_risk"], data["medium_risk"], data["low_risk"]],
                color=["High Risk", "Medium Risk", "Low Risk"],
                color_discrete_map={"High Risk": "#FF4B4B", "Medium Risk": "#FFA500", "Low Risk": "#4BCB9B"},
                labels={"x":"Risk Level", "y":"Number of Customers"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Failed to load analytics")
