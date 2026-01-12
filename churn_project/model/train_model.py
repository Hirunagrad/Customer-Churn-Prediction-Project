import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

df = pd.read_excel("data/cleaned_telco.xlsx")

df = df.drop(columns=[
    'CustomerID','Churn Reason','Lat Long','Count',
    'Country','State','City','Zip Code','Churn Label','Churn Score'
])

X = df.drop("Churn Value", axis=1)
y = df["Churn Value"]

cat_cols = X.select_dtypes(include=["object","bool"]).columns
num_cols = X.select_dtypes(include=["int64","float64"]).columns

preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
])

model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    eval_metric="logloss",
    random_state=42
)

pipeline = ImbPipeline([
    ("prep", preprocess),
    ("smote", SMOTE(random_state=42)),
    ("model", model)
])

pipeline.fit(X, y)

joblib.dump(pipeline, "churn_model.joblib")
print("Model saved successfully")
