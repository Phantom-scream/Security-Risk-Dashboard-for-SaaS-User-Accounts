import os
import csv
import json
from datetime import datetime

def save_report(risks):
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"reports/risk_report_{timestamp}.csv"
    json_file = f"reports/risk_report_{timestamp}.json"

    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["User ID", "Name", "Email", "Risk Score", "Risk Level", "Reasons"])
        for r in risks:
            writer.writerow([
                r["id"],
                r["name"],
                r["email"],
                r["score"],
                r["risk_level"],
                "; ".join(r["reasons"])
            ])

    with open(json_file, "w") as f:
        json.dump(risks, f, indent=4)

    print(f"\n Reports saved:\n- {csv_file}\n- {json_file}")