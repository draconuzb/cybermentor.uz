import requests, re

BASE = "http://8a086c8c-5f4a-4125-b5ff-196cd645b8ce.red.cyberkent.uz"
s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
})

r = s.get(BASE + "/kirish", timeout=10)
print("GET /kirish ->", r.status_code, len(r.text))
apis = sorted(set(re.findall(r'/api/[a-zA-Z0-9/_-]*', r.text)))
print("APIs found:", apis)
with open("/tmp/kirish.html", "w", encoding="utf-8") as f:
    f.write(r.text)

r2 = s.post(BASE + "/api/session", json={}, timeout=10)
print("\nPOST /api/session (browser UA) ->", r2.status_code, r2.text[:300])
