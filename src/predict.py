import pickle
import os

def load_models():
    """Load all saved models"""
    with open('models/priority_model.pkl', 'rb') as f:
        priority_model = pickle.load(f)
    with open('models/severity_model.pkl', 'rb') as f:
        severity_model = pickle.load(f)
    with open('models/tfidf.pkl', 'rb') as f:
        tfidf = pickle.load(f)
    with open('models/le_priority.pkl', 'rb') as f:
        le_priority = pickle.load(f)
    with open('models/le_severity.pkl', 'rb') as f:
        le_severity = pickle.load(f)
    return priority_model, severity_model, tfidf, le_priority, le_severity

def get_fix_time(priority):
    """Estimate fix time based on priority"""
    fix_times = {
        'P1': '1-2 days (Urgent)',
        'P2': '3-5 days (High)',
        'P3': '1-2 weeks (Medium)',
        'P4': '2-4 weeks (Low)'
    }
    return fix_times.get(priority, 'Unknown')

def get_team(text):
    """Assign team based on keywords in bug text"""
    text = text.lower()
    if any(word in text for word in ['frontend', 'ui', 'css', 'html', 'react']):
        return 'Frontend Team'
    elif any(word in text for word in ['database', 'sql', 'db', 'query']):
        return 'Database Team'
    elif any(word in text for word in ['api', 'backend', 'server', 'endpoint']):
        return 'Backend Team'
    elif any(word in text for word in ['pipeline', 'ml', 'model', 'data']):
        return 'ML/Data Team'
    elif any(word in text for word in ['deploy', 'docker', 'cloud', 'devops']):
        return 'DevOps Team'
    else:
        return 'General Engineering Team'

def predict_bug(title, description):
    """Main prediction function"""

    # Load models
    priority_model, severity_model, tfidf, le_priority, le_severity = load_models()

    # Combine text
    text = title + ' ' + description
    text_clean = text.lower()

    # Vectorize
    text_tfidf = tfidf.transform([text_clean])

    # Predict
    priority_encoded = priority_model.predict(text_tfidf)[0]
    severity_encoded = severity_model.predict(text_tfidf)[0]

    # Decode labels
    priority = le_priority.inverse_transform([priority_encoded])[0]
    severity = le_severity.inverse_transform([severity_encoded])[0]

    # Get confidence scores
    priority_conf = max(priority_model.predict_proba(text_tfidf)[0]) * 100
    severity_conf = max(severity_model.predict_proba(text_tfidf)[0]) * 100

    # Get fix time and team
    fix_time = get_fix_time(priority)
    team = get_team(text_clean)

    result = {
        'priority': priority,
        'severity': severity,
        'fix_time': fix_time,
        'assigned_team': team,
        'priority_confidence': round(priority_conf, 2),
        'severity_confidence': round(severity_conf, 2)
    }

    return result

if __name__ == "__main__":
    # Test prediction
    title = "Memory leak in ML pipeline causing OOM error"
    description = "The ML service crashes after 2 hours due to memory not being released properly"

    result = predict_bug(title, description)
    print("\n🐛 Bug Prediction Result:")
    print(f"Priority        : {result['priority']}")
    print(f"Severity        : {result['severity']}")
    print(f"Fix Time        : {result['fix_time']}")
    print(f"Assigned Team   : {result['assigned_team']}")
    print(f"Priority Conf   : {result['priority_confidence']}%")
    print(f"Severity Conf   : {result['severity_confidence']}%")