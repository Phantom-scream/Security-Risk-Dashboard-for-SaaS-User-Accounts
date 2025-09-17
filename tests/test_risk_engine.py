from src.risk_engine import analyze_user_risks

def test_risk_scoring_high_when_multiple_risks():
    users = [{
        "id": "1",
        "full_name": "Test User",
        "email": "user@gmail.com",
        "password": "123456",
        "registered": "2010-01-01T00:00:00Z",
        "country": "Iran",
    }]
    res = analyze_user_risks(users)
    assert res and res[0]["risk_level"] == "HIGH"