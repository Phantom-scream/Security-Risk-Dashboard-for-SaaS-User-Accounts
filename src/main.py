from fetchers.hr_system import fetch_hr_users
from fetchers.cloud_storage import fetch_cloud_users
from risk_engine import analyze_user_risks
from report_generator import save_report
from database import init_db, save_risks_to_db
from alert_system import trigger_alerts

if __name__ == "__main__":
    init_db()

    hr_users = fetch_hr_users()
    hr_risks = analyze_user_risks(hr_users)
    save_report(hr_risks, system_name="HRSystem") 
    save_risks_to_db(hr_risks, system_name="HRSystem")
    trigger_alerts(hr_risks)

    cloud_users = fetch_cloud_users()
    cloud_risks = analyze_user_risks(cloud_users)
    save_report(cloud_risks, system_name="CloudStorage") 
    save_risks_to_db(cloud_risks, system_name="CloudStorage")
    trigger_alerts(cloud_risks)