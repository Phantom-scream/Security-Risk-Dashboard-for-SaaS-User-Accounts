from fetchers.hr_system import fetch_hr_users

if __name__ == "__main__":
    users = fetch_hr_users()
    print(f"\nFetched {len(users)} HR users")

    for u in users[:3]:
        print(f"{u['full_name']} | {u['email']} | Country: {u['country']} | Registered: {u['registered']}")