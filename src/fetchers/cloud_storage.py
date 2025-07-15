import requests

API_URL = "https://randomuser.me/api/?results=15"

def fetch_cloud_users():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        raw_users = response.json()["results"]

        users = []
        for u in raw_users:
            users.append({
                "id": u["login"]["uuid"],
                "username": u["login"]["username"],
                "email": u["email"].replace("@", "+cloud@"), 
                "password": u["login"]["password"],
                "registered": u["registered"]["date"],
                "country": u["location"]["country"],
                "full_name": f"{u['name']['first']} {u['name']['last']}",
                "system": "CloudStorage"
            })

        return users

    except requests.RequestException as e:
        print(f"[CLOUD STORAGE] API Error: {e}")
        return []