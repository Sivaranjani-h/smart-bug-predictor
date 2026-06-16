from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import predict_bug

app = FastAPI(title="Smart Bug Priority Predictor API")

# ✅ Input Model
class BugReport(BaseModel):
    title: str
    description: str

# ✅ Health Check
@app.get("/")
def home():
    return {"message": "Smart Bug Predictor API is running! 🐛"}

# ✅ Predict Endpoint
@app.post("/predict")
def predict(bug: BugReport):
    result = predict_bug(bug.title, bug.description)
    return {
        "status": "success",
        "prediction": result
    }

# ✅ Health Check Endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}