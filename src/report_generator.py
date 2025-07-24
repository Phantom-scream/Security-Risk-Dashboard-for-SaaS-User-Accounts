import os
import csv
import json
from datetime import datetime

def save_report(risks, system_name):
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_system = system_name.replace(" ", "_").lower()

    csv_file = f"reports/{safe_system}_risk_report_{timestamp}.csv"
    json_file = f"reports/{safe_system}_risk_report_{timestamp}.json"

    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["User ID", "Name", "Email", "Risk Score", "Risk Level", "Reasons", "System"])
        for r in risks:
            writer.writerow([
                r["id"],
                r["name"],
                r["email"],
                r["score"],
                r["risk_level"],
                "; ".join(r["reasons"]),
                system_name
            ])

    with open(json_file, "w") as f:  # it tells python to create the file for writing (Pythona file i yaratmaq üçün yazmağı bildirir)
        json.dump(risks, f, indent=4)

    print(f"\n {system_name} Reports saved:")
    print(f"- {csv_file}")
    print(f"- {json_file}")