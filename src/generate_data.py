import pandas as pd
import random
import uuid

bugs = [
    # P1 - Critical
    ("Production server completely down", 
     "Entire production system is down, all users affected, complete outage",
     "Critical", "P1"),
    ("Database corruption detected",
     "Critical data corruption in production database, data loss occurring",
     "Critical", "P1"),
    ("Security breach detected",
     "Unauthorized access detected in production, customer data at risk",
     "Critical", "P1"),
    ("Payment system failure",
     "All payment transactions failing, revenue loss occurring every minute",
     "Critical", "P1"),
    ("API completely unresponsive",
     "All API endpoints returning 503, entire platform down for all users",
     "Critical", "P1"),

    # P2 - High
    ("Login failure for majority of users",
     "70 percent of users unable to login, authentication service failing",
     "High", "P2"),
    ("Data pipeline broken",
     "ML data pipeline stopped processing, model predictions are stale",
     "High", "P2"),
    ("Memory leak causing crashes",
     "Application crashes every 2 hours due to memory not being released",
     "High", "P2"),
    ("Performance degradation in production",
     "Response time increased from 200ms to 10 seconds for all users",
     "High", "P2"),
    ("Docker container crashing on deployment",
     "Kubernetes pod keeps restarting, deployment failing repeatedly",
     "High", "P2"),

    # P3 - Medium
    ("Dashboard charts loading slowly",
     "Analytics dashboard takes 30 seconds to load charts for some users",
     "Medium", "P3"),
    ("Search filter not working correctly",
     "Search results showing incorrect items when multiple filters applied",
     "Medium", "P3"),
    ("Email notifications delayed",
     "Email notifications are being delivered 2 hours late occasionally",
     "Medium", "P3"),
    ("Export to CSV missing some columns",
     "When exporting data to CSV some columns are missing from the file",
     "Medium", "P3"),
    ("UI misalignment on mobile devices",
     "Navigation menu overlaps content on mobile screens smaller than 375px",
     "Medium", "P3"),

    # P4 - Low
    ("Typo in settings page label",
     "Small spelling mistake in settings page, no functional impact",
     "Low", "P4"),
    ("Button color inconsistency",
     "Submit button color is slightly different shade on one page only",
     "Low", "P4"),
    ("Tooltip text outdated",
     "Help tooltip shows outdated text, functionality works correctly",
     "Low", "P4"),
    ("Minor padding issue in footer",
     "Footer padding is 2px off on desktop, purely cosmetic issue",
     "Low", "P4"),
    ("Console warning in browser",
     "Non critical console warning appearing, no user impact at all",
     "Low", "P4"),
]

# Generate 1000 rows
rows = []
for i in range(1000):
    bug = random.choice(bugs)
    rows.append({
        'bug_id': str(uuid.uuid4()),
        'title': bug[0],
        'description': bug[1],
        'severity': bug[2],
        'priority': bug[3],
        'product_module': random.choice([
            'Data-Pipeline', 'ML-Service', 
            'WebApp-Core', 'Auth-Service', 'API-Gateway'
        ]),
        'environment': random.choice(['Production', 'Staging', 'Development']),
        'status': random.choice(['Open', 'In Progress', 'Resolved'])
    })

df = pd.DataFrame(rows)
df.to_csv('data/raw/bugs.csv', index=False)
print(f"✅ Generated {len(df)} balanced bug records!")
print(df['priority'].value_counts())
print(df['severity'].value_counts())