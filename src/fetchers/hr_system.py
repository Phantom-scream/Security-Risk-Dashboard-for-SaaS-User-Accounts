import requests

API_URL = "https://randomuser.me/api/?results=20"

def fetch_hr_users():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        raw_users = response.json()["results"]

        normalized_users = []

        for user in raw_users:
            normalized_users.append({
                "id": user["login"]["uuid"],
                "username": user["login"]["username"],
                "email": user["email"],
                "password": user["login"]["password"],
                "registered": user["registered"]["date"],
                "country": user["location"]["country"],
                "first_name": user["name"]["first"],
                "last_name": user["name"]["last"],
                "full_name": f"{user['name']['first']} {user['name']['last']}",
                "picture": user["picture"]["thumbnail"]
            })

        return normalized_users

    except requests.RequestException as e:
        print(f"[HR SYSTEM] API Error: {e}")
        return []