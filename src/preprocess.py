import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def clean_text(text):
    """Clean bug report text"""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_data():
    """Load raw dataset"""
    df = pd.read_csv('data/raw/bugs.csv')
    print(f"[ok] Loaded {len(df)} bug reports")
    return df

def preprocess(df):
    """Clean and prepare data"""

    # Combine title + description as input text
    df['text'] = df['title'] + ' ' + df['description']
    df['text'] = df['text'].apply(clean_text)

    # Clean priority column (P1,P2,P3,P4 → 0,1,2,3)
    le_priority = LabelEncoder()
    df['priority_encoded'] = le_priority.fit_transform(df['priority'])

    # Clean severity column
    le_severity = LabelEncoder()
    df['severity_encoded'] = le_severity.fit_transform(df['severity'])

    # Save label encoders
    os.makedirs('models', exist_ok=True)
    with open('models/le_priority.pkl', 'wb') as f:
        pickle.dump(le_priority, f)
    with open('models/le_severity.pkl', 'wb') as f:
        pickle.dump(le_severity, f)

    print("[ok] Preprocessing done!")
    print(f"Priority classes: {le_priority.classes_}")
    print(f"Severity classes: {le_severity.classes_}")

    return df

def save_processed(df):
    """Save cleaned data"""
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/bugs_clean.csv', index=False)
    print("[ok] Saved to data/processed/bugs_clean.csv")

if __name__ == "__main__":
    df = load_data()
    df = preprocess(df)
    save_processed(df)