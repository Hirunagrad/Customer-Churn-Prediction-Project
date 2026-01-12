# Project Overview

This project focuses on predicting customer churn in the telecom industry using machine learning.
The goal is to identify high-risk customers early and support data-driven retention strategies.

# The project includes:

Data preprocessing and feature engineering

Machine learning model training and evaluation

A REST API built with FastAPI

An interactive dashboard built with Streamlit

# Key Features

Cleaned and preprocessed real-world telecom dataset

Handles categorical encoding, scaling, and class imbalance

Trained multiple models and compared performance

REST API for churn prediction

Dashboard to visualize churn probability for a single customer

# Project Structure
churn_project/
├── .venv/                 
├── backend/
│   └── api.py
├── dashboard/
│   └── app.py
├── model/
│   └── train_model.py
├── data/
│   └── cleaned_telco.xlsx
├── requirements.txt
├── .gitignore
└── README.md

# Requirements
## System Requirements

Python 3.10 or 3.11 (recommended)

Git

macOS / Windows / Linux

## Python Libraries Used

pandas

numpy

scikit-learn

imbalanced-learn

xgboost

fastapi

uvicorn

streamlit

requests

joblib

openpyxl

(All are included in requirements.txt)

# Installation & Setup (Step-by-Step)

Clone the Repository
git clone https://github.com/<your-username>/Customer-Churn-Prediction-Project.git
cd Customer-Churn-Prediction-Project/churn_project

Go to the project folder and open a terminal and create Virtual Environment
python -m venv .venv

Activate it:

macOS / Linux

source .venv/bin/activate

Windows

.venv\Scripts\activate

Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

Prepare the Dataset

Place the cleaned dataset file in:

churn_project/data/cleaned_telco.xlsx


Dataset is not included in GitHub (intentionally).

Model Training (Optional)

If you want to retrain the model:

python model/train_model.py


This will:

Preprocess the data

Train the model

Save the trained model as churn_model.joblib

#Run Backend API (FastAPI)

From the project root:

uvicorn backend.api:app --reload


Backend will run at:

http://127.0.0.1:8000


Swagger API Docs:

http://127.0.0.1:8000/docs

#Run Dashboard (Streamlit)

Open a new terminal, activate the virtual environment again, then run:

streamlit run dashboard/app.py


Dashboard will open at:

http://localhost:8501

# How the System Works

1.User enters customer details in Streamlit dashboard

2.Dashboard sends input to FastAPI /predict endpoint

3.API applies the same preprocessing pipeline

4.Model predicts churn probability

5.Dashboard displays:

Churn probability

Churn risk (Yes / No)
 
Example Input Fields

Gender

Senior Citizen

Partner

Dependents

Tenure Months

Monthly Charges

Total Charges

Contract Type

Payment Method

CLTV

Location (Latitude, Longitude)

 Example Output
{
"churn_probability": 0.67,
"prediction": 1
}


prediction = 1 → High churn risk

prediction = 0 → Low churn risk

# Team Collaboration Notes

Always activate virtual environment before running code

Do NOT commit datasets or trained model files

Use requirements.txt for dependency sync

Use Git branches for development

# Academic Notes

Recall was prioritized over precision to better detect churners

Multiple models were evaluated and compared

Architecture follows real-world ML deployment practices
 
# Future Improvements

User authentication

Model monitoring

Cloud deployment

Batch predictions

# License
This project is developed for academic purposes.