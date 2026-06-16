from prefect import flow, task
import subprocess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.monitor import run_monitoring

@task(name="Check Data Drift")
def check_drift():
    """Check if data drift is detected"""
    print("🔍 Checking for data drift...")
    drift_detected = run_monitoring()
    return drift_detected

@task(name="Preprocess Data")
def preprocess_data():
    """Run data preprocessing"""
    print("⚙️ Preprocessing data...")
    result = subprocess.run(
        ['python', 'src/preprocess.py'],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Preprocessing failed: {result.stderr}")
    print("✅ Preprocessing complete!")

@task(name="Retrain Model")
def retrain_model():
    """Retrain the ML model"""
    print("🤖 Retraining model...")
    result = subprocess.run(
        ['python', 'src/train.py'],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Training failed: {result.stderr}")
    print("✅ Model retrained successfully!")

@task(name="Validate Model")
def validate_model():
    """Validate retrained model"""
    print("✅ Validating model...")
    from src.predict import predict_bug
    test_result = predict_bug(
        "Production server down",
        "Critical failure all users affected"
    )
    print(f"Test prediction: {test_result}")
    print("✅ Model validation passed!")
    return test_result

@flow(name="Smart Bug Predictor - Retrain Pipeline")
def retrain_pipeline(force_retrain: bool = False):
    """
    Main retraining pipeline:
    1. Check drift
    2. If drift detected → retrain
    3. Validate new model
    """
    print("🚀 Starting Retraining Pipeline...")
    print("=" * 50)

    # Step 1 - Check Drift
    drift_detected = check_drift()

    # Step 2 - Retrain if drift detected or forced
    if drift_detected or force_retrain:
        print("⚠️ Retraining triggered!")
        preprocess_data()
        retrain_model()
        validate_model()
        print("🎉 Pipeline completed - Model updated!")
    else:
        print("✅ No drift detected - Model is stable!")
        print("⏭️ Skipping retraining...")

    print("=" * 50)
    print("✅ Pipeline finished!")

if __name__ == "__main__":
    # Run pipeline
    retrain_pipeline(force_retrain=True)