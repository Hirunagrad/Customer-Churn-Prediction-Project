from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()
model = joblib.load("churn_model.joblib")

class CustomerInput(BaseModel):
    Gender: str
    Senior_Citizen: str
    Partner: str
    Dependents: str
    Tenure_Months: int
    Phone_Service: str
    Multiple_Lines: str
    Internet_Service: str
    Online_Security: str
    Online_Backup: str
    Device_Protection: str
    Tech_Support: str
    Streaming_TV: str
    Streaming_Movies: str
    Contract: str
    Paperless_Billing: str
    Payment_Method: str
    Monthly_Charges: float
    Total_Charges: float
    CLTV: float


@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/predict")
def predict(customer: CustomerInput):
    df = pd.DataFrame([customer.model_dump()])

    # Rename columns to match training
    df = df.rename(columns={
        "Senior_Citizen": "Senior Citizen",
        "Tenure_Months": "Tenure Months",
        "Phone_Service": "Phone Service",
        "Multiple_Lines": "Multiple Lines",
        "Internet_Service": "Internet Service",
        "Online_Security": "Online Security",
        "Online_Backup": "Online Backup",
        "Device_Protection": "Device Protection",
        "Tech_Support": "Tech Support",
        "Streaming_TV": "Streaming TV",
        "Streaming_Movies": "Streaming Movies",
        "Paperless_Billing": "Paperless Billing",
        "Payment_Method": "Payment Method",
        "Monthly_Charges": "Monthly Charges",
        "Total_Charges": "Total Charges"
    })

    # ADD MISSING NUMERIC FEATURES
    df["Latitude"] = 0.0
    df["Longitude"] = 0.0

    prob = float(model.predict_proba(df)[0][1])

    return {
        "churn_probability": round(prob, 3),
        "prediction": int(prob > 0.5)
    }
