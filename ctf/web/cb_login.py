import requests

BASE = "http://8a086c8c-5f4a-4125-b5ff-196cd645b8ce.red.cyberkent.uz"
s = requests.Session()

candidates = [
    "/api/login",
    "/api/auth/login",
    "/api/auth/signin",
    "/api/user/login",
    "/api/session",
]

for path in candidates:
    try:
        r = s.post(BASE + path, json={"email": "mijoz@cyberbank.uz", "password": "Mijoz#2026"}, timeout=10)
        print(path, r.status_code, r.text[:300])
    except Exception as e:
        print(path, "ERR", e)
