import joblib
import os

MODEL_PATH = "ml/model.pkl"
VECTORIZER_PATH = "ml/vectorizer.pkl"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_scam(text: str):
    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0][1]  

    return {
        "ml_probability": float(prob),
        "ml_prediction": "SCAM" if prob > 0.5 else "LEGIT"
    }