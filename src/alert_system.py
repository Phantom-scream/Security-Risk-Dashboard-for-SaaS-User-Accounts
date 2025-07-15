def trigger_alerts(risks, threshold=3):
    high_risk_users = [r for r in risks if r["risk_level"] == "HIGH"]

    if len(high_risk_users) >= threshold:
        print(f"\n ALERT: {len(high_risk_users)} HIGH-RISK USERS DETECTED!")
        for user in high_risk_users:
            print(f"  - {user['name']} ({user['email']}) | Score: {user['score']}")
    else:
        print("\n Risk level acceptable. No alert triggered.")