#!/bin/bash
# vpn_helpers.sh — CyberKent VPN uchun connect/status yordamchilarini serverga o'rnatadi
set -u
mkdir -p ~/.local/bin ~/ctf

# --- vpn-connect ---
cat > ~/.local/bin/vpn-connect <<'EOF'
#!/bin/bash
# vpn-connect [config.ovpn] — CyberKent VPN'ga ulanadi (default ~/cyberkent.ovpn)
OVPN="${1:-$HOME/cyberkent.ovpn}"
if [ ! -f "$OVPN" ]; then
  echo "❌ Config topilmadi: $OVPN"
  echo "   code-server Explorer'ga .ovpn faylni tashlang, keyin: vpn-connect ~/<fayl>.ovpn"
  exit 1
fi
sudo pkill -f 'openvpn --config' 2>/dev/null; sleep 1
echo "🔌 Ulanmoqda: $OVPN"
sudo openvpn --config "$OVPN" --daemon --log "$HOME/vpn.log" --writepid "$HOME/vpn.pid"
for i in $(seq 1 15); do
  sleep 1
  if grep -q "Initialization Sequence Completed" "$HOME/vpn.log" 2>/dev/null; then break; fi
done
echo "----- vpn.log (oxiri) -----"
tail -6 "$HOME/vpn.log"
IP=$(ip -4 addr show tun0 2>/dev/null | grep -oP 'inet \K[0-9.]+')
if [ -n "$IP" ]; then
  echo "======================================"
  echo " ✅ ULANDI! ATTACK IP (LHOST) = $IP"
  echo "======================================"
else
  echo "⚠ tun0 hali yo'q — vpn.log'ni tekshiring (vpn-log)"
fi
EOF

# --- vpn-ip ---
cat > ~/.local/bin/vpn-ip <<'EOF'
#!/bin/bash
ip -4 addr show tun0 2>/dev/null | grep -oP 'inet \K[0-9.]+' || echo "tun0 yo'q (VPN ulanmagan)"
EOF

# --- vpn-status ---
cat > ~/.local/bin/vpn-status <<'EOF'
#!/bin/bash
if pgrep -f 'openvpn --config' >/dev/null; then
  echo "🟢 VPN ISHLAYAPTI  |  IP: $(ip -4 addr show tun0 2>/dev/null | grep -oP 'inet \K[0-9.]+')"
  ip route | grep tun0
else
  echo "🔴 VPN ulanmagan"
fi
EOF

# --- vpn-log ---
cat > ~/.local/bin/vpn-log <<'EOF'
#!/bin/bash
tail -${1:-20} "$HOME/vpn.log"
EOF

# --- vpn-off ---
cat > ~/.local/bin/vpn-off <<'EOF'
#!/bin/bash
sudo pkill -f 'openvpn --config' && echo "VPN uzildi" || echo "VPN ishlamayotgan edi"
EOF

chmod +x ~/.local/bin/vpn-connect ~/.local/bin/vpn-ip ~/.local/bin/vpn-status ~/.local/bin/vpn-log ~/.local/bin/vpn-off

# --- Qo'llanma ---
cat > ~/ctf/README.txt <<'EOF'
=== CYBERKENT CTF — HUJUM BAZASI (cybermentor server) ===

10:00'da red.cyberkent.uz/vpn dan shaxsiy .ovpn'ni yuklab oling.

1) .ovpn ni serverga qo'ying:
   - code-server Explorer'ga drag-drop qiling (~/ ga), yoki
   - nomini cyberkent.ovpn qiling

2) Ulaning:
   vpn-connect ~/cyberkent.ovpn
   -> "ATTACK IP (LHOST) = 10.x.x.x" chiqadi. Shu sizning IP.

3) Foydali buyruqlar:
   vpn-status    -> ulanish holati + IP
   vpn-ip        -> faqat attack IP (reverse shell LHOST)
   vpn-log       -> VPN loglari
   vpn-off       -> uzish

4) Hujum (target IP = panelдan):
   nmap -sVC -T4 <target>
   ffuf -u http://<target>/FUZZ -w ~/wordlists/common.txt
   Reverse shell LHOST = `vpn-ip` natijasi, listener: nc -lvnp 4444

Asboblar: nmap ffuf gobuster sqlmap nikto hydra john hashcat gdb+GEF
radare2 binwalk exiftool steghide zsteg stegseek volatility3(vol) impacket
RsaCtfTool nth ROPgadget one_gadget + CyberChef: /cyberchef/
EOF

echo "✅ VPN helperlar o'rnatildi:"
ls -1 ~/.local/bin/vpn-* | sed 's/^/  /'
echo "✅ Qo'llanma: ~/ctf/README.txt"
echo "-- tekshiruv: openvpn = $(command -v openvpn)"
