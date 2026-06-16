import pandas as pd
import pickle
import os
import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils.class_weight import compute_class_weight

def train():
    # Load preprocessed data
    df = pd.read_csv('data/processed/bugs_clean.csv')
    print(f"[OK] Loaded {len(df)} records")

    # Features & Labels
    X = df['text']
    y_priority = df['priority_encoded']
    y_severity = df['severity_encoded']

    # Train/Test Split
    X_train, X_test, yp_train, yp_test = train_test_split(
        X, y_priority, test_size=0.2, random_state=42
    )
    _, _, ys_train, ys_test = train_test_split(
        X, y_severity, test_size=0.2, random_state=42
    )

    # TF-IDF Vectorizer
    tfidf = TfidfVectorizer(max_features=5000)
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    # Fix class imbalance for Priority Model
    priority_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(yp_train),
        y=yp_train
    )
    priority_weight_dict = dict(enumerate(priority_weights))

    # Fix class imbalance for Severity Model
    severity_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(ys_train),
        y=ys_train
    )
    severity_weight_dict = dict(enumerate(severity_weights))

    # Start MLflow Experiment
    mlflow.set_experiment("smart-bug-predictor")

    with mlflow.start_run():

        # Train Priority Model
        priority_model = RandomForestClassifier(
            n_estimators=200,
            class_weight=priority_weight_dict,
            random_state=42
        )
        priority_model.fit(X_train_tfidf, yp_train)
        priority_preds = priority_model.predict(X_test_tfidf)
        priority_acc = accuracy_score(yp_test, priority_preds)

        # Train Severity Model
        severity_model = RandomForestClassifier(
            n_estimators=200,
            class_weight=severity_weight_dict,
            random_state=42
        )
        severity_model.fit(X_train_tfidf, ys_train)
        severity_preds = severity_model.predict(X_test_tfidf)
        severity_acc = accuracy_score(ys_test, severity_preds)

        # Log Metrics in MLflow
        mlflow.log_param("model", "RandomForest")
        mlflow.log_param("n_estimators", 200)
        mlflow.log_metric("priority_accuracy", priority_acc)
        mlflow.log_metric("severity_accuracy", severity_acc)

        print(f"[OK] Priority Accuracy: {priority_acc:.2f}")
        print(f"[OK] Severity Accuracy: {severity_acc:.2f}")
        print("\nPriority Report:")
        print(classification_report(yp_test, priority_preds))

        # Save Models
        os.makedirs('models', exist_ok=True)
        with open('models/priority_model.pkl', 'wb') as f:
            pickle.dump(priority_model, f)
        with open('models/severity_model.pkl', 'wb') as f:
            pickle.dump(severity_model, f)
        with open('models/tfidf.pkl', 'wb') as f:
            pickle.dump(tfidf, f)

        # Log Models in MLflow
        mlflow.sklearn.log_model(priority_model, "priority_model")
        mlflow.sklearn.log_model(severity_model, "severity_model")

        print("[OK] Models saved successfully!")

if __name__ == "__main__":
    train()