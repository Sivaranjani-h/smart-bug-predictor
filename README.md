# 🎯 BugRadar — Smart Bug Priority Predictor

An MLOps-powered web application that automatically 
classifies bug reports by priority, severity, fix time 
and assigns the right team using NLP + Machine Learning.

## 🚀 Features
- Single bug classification
- Bulk CSV upload & classify
- Real-time dashboard
- MLflow experiment tracking
- Evidently AI drift monitoring
- Prefect auto retraining pipeline
- DVC data versioning
- Docker containerization

## 🛠️ Tech Stack
- Frontend: Streamlit + Plotly
- Backend: FastAPI
- ML: RandomForest + TF-IDF
- MLOps: MLflow + DVC + Prefect + Evidently
- Deploy: Docker + GitHub Actions

## ⚙️ How to Run

### 1. Clone the repo
git clone https://github.com/yourusername/smart-bug-predictor

### 2. Install dependencies
pip install -r requirements.txt

### 3. Generate & prepare data
python src/generate_data.py
python src/preprocess.py

### 4. Train model
python src/train.py

### 5. Run app
streamlit run app/streamlit_app.py

## 📁 Project Structure
smart-bug-predictor/
├── src/          → ML code
├── app/          → Frontend + Backend
├── pipelines/    → Prefect pipeline
├── data/         → Dataset (gitignored)
├── models/       → Saved models (gitignored)
└── Dockerfile    → Container config

## 🔁 MLOps Pipeline
1. Data versioning with DVC
2. Experiment tracking with MLflow  
3. Drift detection with Evidently AI
4. Auto retraining with Prefect
5. CI/CD with GitHub Actions
