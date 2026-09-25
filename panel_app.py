#!/usr/bin/env python3
# CyberKent Red Team — cybermentor boshqaruv paneli
import os, subprocess, json, functools, secrets, re
from flask import Flask, request, session, redirect, Response, jsonify

app = Flask(__name__)
CFG = os.path.expanduser("~/.panel")
os.makedirs(CFG, exist_ok=True)
sk = os.path.join(CFG, "secret")
if not os.path.exists(sk):
    open(sk, "w").write(secrets.token_hex(32))
app.secret_key = open(sk).read().strip()
PW_FILE = os.path.join(CFG, "pass")
PASSWORD = open(PW_FILE).read().strip() if os.path.exists(PW_FILE) else "changeme"

def sh(cmd, timeout=20):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout).stdout.strip()
    except Exception as e:
        return f"err: {e}"

def login_required(f):
    @functools.wraps(f)
    def w(*a, **k):
        if not session.get("ok"):
            return redirect("login")
        return f(*a, **k)
    return w

@app.route("/login", methods=["GET", "POST"])
def login():
    err = ""
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["ok"] = True
            return redirect(".")
        err = "❌ Noto'g'ri parol"
        # log the attempt
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        open(os.path.join(CFG, "attempts.log"), "a").write(f"{sh('date +%H:%M:%S')} FAIL {ip}\n")
    return Response(LOGIN_HTML.replace("{{err}}", err), mimetype="text/html")

@app.route("/logout")
def logout():
    session.clear(); return redirect("login")

@app.route("/")
@login_required
def index():
    return Response(DASH_HTML, mimetype="text/html")

@app.route("/api/status")
@login_required
def status():
    tun = sh("ip -4 addr show tun0 2>/dev/null | grep -oP 'inet \\K[0-9.]+'")
    vpn_up = bool(tun)
    svcs = {s: sh(f"systemctl is-active {s} 2>/dev/null") for s in
            ["code-server@ubuntu", "nginx", "filebrowser", "fail2ban"]}
    # xavfsizlik: muvaffaqiyatsiz SSH loginlar
    failed = sh("sudo grep -c 'Failed password' /var/log/auth.log 2>/dev/null || echo 0")
    lastb = sh("sudo lastb -n 5 2>/dev/null | head -5")
    banned = sh("sudo fail2ban-client status sshd 2>/dev/null | grep -i 'banned IP' || echo '-'")
    attempts = sh(f"tail -5 {os.path.join(CFG,'attempts.log')} 2>/dev/null")
    flags = sh("cat ~/ctf/flags.txt 2>/dev/null")
    targets = sh("ls ~/ctf/targets 2>/dev/null | tr '\\n' ' '")
    ovpn = "bor" if os.path.exists(os.path.expanduser("~/cyberkent.ovpn")) else "yo'q (yuklang)"
    return jsonify(dict(vpn_up=vpn_up, attack_ip=tun or "-", svcs=svcs,
                        failed=failed, lastb=lastb, banned=banned, attempts=attempts,
                        flags=flags or "(hali yo'q)", targets=targets or "-", ovpn=ovpn))

@app.route("/api/vpn/<action>", methods=["POST"])
@login_required
def vpn(action):
    if action == "connect":
        cfg = os.path.expanduser("~/cyberkent.ovpn")
        if not os.path.exists(cfg):
            return jsonify(msg="❌ ~/cyberkent.ovpn topilmadi. Avval .ovpn yuklang.")
        sh("sudo pkill -f 'openvpn --config' 2>/dev/null; sleep 1")
        sh(f"sudo openvpn --config {cfg} --daemon --log /home/ubuntu/vpn.log --writepid /home/ubuntu/vpn.pid", timeout=10)
        return jsonify(msg="🔌 Ulanmoqda... 8s kutib holatni yangilang")
    if action == "disconnect":
        sh("sudo pkill -f 'openvpn --config'")
        return jsonify(msg="🔴 VPN uzildi")
    return jsonify(msg="?")

LOGIN_HTML = """<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>CyberKent // Kirish</title><style>
*{box-sizing:border-box}body{background:#0a0e0a;color:#00ff41;font-family:'Courier New',monospace;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
.box{border:1px solid #00ff41;padding:40px;box-shadow:0 0 30px #00ff4133;width:340px;max-width:90vw}
h1{font-size:20px;letter-spacing:2px;text-align:center}.sub{color:#0a8;font-size:11px;text-align:center;margin-bottom:20px}
input{width:100%;background:#000;border:1px solid #00ff41;color:#00ff41;padding:12px;font-family:inherit;margin:8px 0}
button{width:100%;background:#00ff41;color:#000;border:0;padding:12px;font-weight:bold;cursor:pointer;font-family:inherit}
.err{color:#ff3355;font-size:12px;text-align:center;margin-top:8px}</style></head>
<body><form class=box method=post><h1>&#9760; CYBERKENT RED TEAM</h1><div class=sub>cybermentor // secure access</div>
<input type=password name=password placeholder="parol" autofocus><button>KIRISH</button><div class=err>{{err}}</div></form></body></html>"""

DASH_HTML = """<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>CyberKent // Panel</title><style>
*{box-sizing:border-box}body{background:#0a0e0a;color:#c8ffd0;font-family:'Courier New',monospace;margin:0;padding:16px}
a{color:#00ff41;text-decoration:none}h1{color:#00ff41;letter-spacing:2px;font-size:22px;margin:4px 0}
.top{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #00ff4133;padding-bottom:10px;margin-bottom:16px;flex-wrap:wrap;gap:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.card{border:1px solid #00ff4133;padding:14px;background:#0d130d}
.card h2{color:#00ff41;font-size:13px;letter-spacing:1px;margin:0 0 10px;border-bottom:1px dashed #00ff4122;padding-bottom:6px}
.big{font-size:20px;font-weight:bold}.on{color:#00ff41}.off{color:#ff3355}
button{background:#00ff41;color:#000;border:0;padding:8px 14px;font-family:inherit;font-weight:bold;cursor:pointer;margin:3px}
button.red{background:#ff3355;color:#fff}pre{white-space:pre-wrap;font-size:11px;color:#7fd68f;margin:6px 0;max-height:120px;overflow:auto}
.links a{display:inline-block;border:1px solid #00ff41;padding:8px 12px;margin:4px 4px 0 0}
.pill{padding:2px 8px;border-radius:10px;font-size:11px}.pillon{background:#00ff4122;color:#00ff41}.pilloff{background:#ff335522;color:#ff3355}
</style></head><body>
<div class=top><h1>&#9760; CYBERKENT RED TEAM PANEL</h1><div><span id=clock></span> &nbsp; <a href=logout>[chiqish]</a></div></div>
<div class=grid>
<div class=card><h2>&#128225; VPN — HUJUM ULANISHI</h2>
  <div>Holat: <span id=vpnstate class=big>...</span></div>
  <div>Attack IP (LHOST): <span id=attackip class=big>-</span></div>
  <div style=margin-top:6px>.ovpn: <span id=ovpn>-</span></div>
  <div style=margin-top:10px><button onclick=vpnAct('connect')>CONNECT</button><button class=red onclick=vpnAct('disconnect')>DISCONNECT</button></div>
  <div id=vpnmsg style=color:#ffd23f;font-size:12px;margin-top:6px></div></div>
<div class=card><h2>&#9881; XIZMATLAR</h2><div id=svcs>...</div></div>
<div class=card><h2>&#128737; XAVFSIZLIK</h2>
  <div>Muvaffaqiyatsiz SSH loginlar: <span id=failed class=big>-</span></div>
  <div>Fail2ban: <span id=banned>-</span></div>
  <div style=margin-top:6px>Oxirgi urinishlar (lastb):</div><pre id=lastb>-</pre>
  <div>Panel login urinishlari:</div><pre id=attempts>-</pre></div>
<div class=card><h2>&#127919; TARGETLAR & FLAGLAR</h2>
  <div>Skanlangan targetlar: <span id=targets>-</span></div>
  <div style=margin-top:6px>Topilgan flaglar:</div><pre id=flags>-</pre></div>
<div class=card><h2>&#128279; TEZ HAVOLALAR</h2><div class=links>
  <a href="/" >IDE (code-server)</a><a href="/files/">Fayllar</a><a href="/cyberchef/">CyberChef</a>
  <a href="https://red.cyberkent.uz" target=_blank>red.cyberkent.uz</a></div>
  <div style=margin-top:10px;font-size:11px;color:#7fd68f>Terminal buyruqlari: vpn-connect · recon &lt;ip&gt; · revshell · listen · serve · flag</div></div>
</div>
<script>
function clk(){document.getElementById('clock').textContent=new Date().toLocaleTimeString()}
setInterval(clk,1000);clk();
async function load(){
 let r=await fetch('api/status');let d=await r.json();
 let v=document.getElementById('vpnstate');v.textContent=d.vpn_up?'🟢 ULANGAN':'🔴 UZILGAN';v.className='big '+(d.vpn_up?'on':'off');
 document.getElementById('attackip').textContent=d.attack_ip;
 document.getElementById('ovpn').textContent=d.ovpn;
 document.getElementById('failed').textContent=d.failed;
 document.getElementById('banned').textContent=d.banned;
 document.getElementById('lastb').textContent=d.lastb||'-';
 document.getElementById('attempts').textContent=d.attempts||'(yo\\'q)';
 document.getElementById('targets').textContent=d.targets;
 document.getElementById('flags').textContent=d.flags;
 let s='';for(let k in d.svcs){let up=d.svcs[k]=='active';s+=`<div>${k.replace('@ubuntu','')} <span class="pill ${up?'pillon':'pilloff'}">${d.svcs[k]}</span></div>`}
 document.getElementById('svcs').innerHTML=s;
}
async function vpnAct(a){document.getElementById('vpnmsg').textContent='...';let r=await fetch('api/vpn/'+a,{method:'POST'});let d=await r.json();document.getElementById('vpnmsg').textContent=d.msg;setTimeout(load,8000)}
load();setInterval(load,7000);
</script></body></html>"""

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8090)
