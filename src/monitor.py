import pandas as pd
import os
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import ColumnDriftMetric

def run_monitoring():
    """Run data drift monitoring"""

    # ✅ Load reference data (training data)
    reference = pd.read_csv('data/processed/bugs_clean.csv')

    # ✅ Simulate new incoming data
    # In production this would be real new bug reports
    new_data = reference.sample(n=200, random_state=99)

    # ✅ Select only text features for monitoring
    cols = ['priority_encoded', 'severity_encoded']
    ref = reference[cols]
    curr = new_data[cols]

    # ✅ Create Drift Report
    report = Report(metrics=[
        DataDriftPreset(),
        DataQualityPreset(),
        ColumnDriftMetric(column_name='priority_encoded'),
        ColumnDriftMetric(column_name='severity_encoded'),
    ])

    # ✅ Run Report
    report.run(
        reference_data=ref,
        current_data=curr
    )

    # ✅ Save Report as HTML
    os.makedirs('reports', exist_ok=True)
    report.save_html('reports/drift_report.html')
    print("✅ Drift report saved to reports/drift_report.html")

    # ✅ Check if drift detected
    report_dict = report.as_dict()
    drift_detected = False

    for metric in report_dict['metrics']:
        if 'drift_detected' in str(metric):
            if metric.get('result', {}).get('drift_detected'):
                drift_detected = True
                break

    if drift_detected:
        print("⚠️ Data drift detected! Model retraining recommended!")
    else:
        print("✅ No significant drift detected. Model is stable!")

    return drift_detected

if __name__ == "__main__":
    run_monitoring()