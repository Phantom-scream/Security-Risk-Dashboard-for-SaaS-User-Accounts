from fetchers.hr_system import fetch_hr_users
from risk_engine import analyze_user_risks
from report_generator import save_report

if __name__ == "__main__":
    users = fetch_hr_users()
    print(f"\nFetched {len(users)} HR users")

    risks = analyze_user_risks(users)

    print("\n Risk Assessment Results:")
    for r in risks:
        print(f"{r['name']} - Risk: {r['risk_level']} (Score: {r['score']})")
        for reason in r["reasons"]:
            print(f"  • {reason}")
        print()

    save_report(risks)