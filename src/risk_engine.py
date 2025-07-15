from datetime import datetime
from dateutil import parser 

COMMON_WEAK_PASSWORDS = {"123456", "password", "qwerty", "letmein", "admin"}
PUBLIC_EMAIL_DOMAINS = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com"}
RISKY_COUNTRIES = {"North Korea", "Iran", "Russia"}

def analyze_user_risks(users):
    results = []

    for user in users:
        score = 0
        reasons = []

        if len(user["password"]) < 8:
            score += 4
            reasons.append("Password too short")

        if user["password"].lower() in COMMON_WEAK_PASSWORDS:
            score += 6
            reasons.append("Common weak password")

        domain = user["email"].split("@")[-1]
        if domain in PUBLIC_EMAIL_DOMAINS:
            score += 2
            reasons.append("Public email domain")

        try:
            reg_date = parser.isoparse(user["registered"])
            if (datetime.now() - reg_date).days > 365 * 5:
                score += 4
                reasons.append("User registered over 5 years ago")
        except Exception:
            reasons.append("Invalid registration date format")

        if user["country"] in RISKY_COUNTRIES:
            score += 5
            reasons.append(f"User from high-risk country: {user['country']}")

        if score >= 10:
            level = "HIGH"
        elif score >= 5:
            level = "MEDIUM"
        else:
            level = "LOW"

        results.append({
            "id": user["id"],
            "name": user["full_name"],
            "email": user["email"],
            "score": score,
            "risk_level": level,
            "reasons": reasons
        })

    return results