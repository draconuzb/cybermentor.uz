import requests

BASE = "http://8a086c8c-5f4a-4125-b5ff-196cd645b8ce.red.cyberkent.uz"
s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
})

r = s.get(BASE + "/", timeout=10)
print("GET / ->", r.status_code)
print("Cookies:", s.cookies.get_dict())
print("Set-Cookie header:", r.headers.get("Set-Cookie"))

r2 = s.get(BASE + "/api/session", timeout=10)
print("\nGET /api/session ->", r2.status_code, r2.text[:400])

r3 = s.get(BASE + "/login", timeout=10)
print("\nGET /login ->", r3.status_code, len(r3.text))
print("Cookies after login page:", s.cookies.get_dict())
