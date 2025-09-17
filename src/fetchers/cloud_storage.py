import requests
from .http import get_session

API_URL = "https://randomuser.me/api/"

def fetch_cloud_users(results=120):
    try:
        session = get_session()
        response = session.get(API_URL, params={"results": results})
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