#!/bin/bash
# ctf_vpn.sh — OpenVPN client + PATH tuzatish + pip toollarni tekshirish
set -u
export DEBIAN_FRONTEND=noninteractive
export PATH="$HOME/.local/bin:$PATH"

echo "[1] OpenVPN client + easy-rsa..."
sudo apt-get install -y -qq openvpn easy-rsa >/dev/null 2>&1 && echo "  ✓ $(openvpn --version 2>/dev/null | head -1 | cut -d' ' -f1-2)"
# TUN qurilma bormi (VPN uchun shart)
[ -c /dev/net/tun ] && echo "  ✓ /dev/net/tun bor (VPN ishlaydi)" || echo "  ⚠ /dev/net/tun yo'q"

echo "[2] PATH doimiy (~/.local/bin)..."
grep -q '.local/bin' ~/.bashrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo "  ✓ bashrc'ga qo'shildi"

echo "[3] pip toollarni qayta o'rnatish (vol, nth, ROPgadget)..."
python3 -m pip install --break-system-packages -q volatility3 name-that-hash ROPgadget 2>&1 | grep -iE 'error|success' | tail -2 || true

echo "[4] pwntools (apt unicorn bilan)..."
python3 -c "import unicorn; print('  unicorn:', unicorn.__version__)" 2>&1 | tail -1
python3 -m pip install --break-system-packages -q pwntools 2>&1 | grep -iE 'error|success|already' | tail -1 || true

echo
echo "==== TEKSHIRUV ===="
for t in openvpn vol nth ROPgadget one_gadget zsteg stegseek hashcat; do
  command -v "$t" >/dev/null 2>&1 && printf "  ✓ %s\n" "$t" || printf "  ✗ %s\n" "$t"
done
python3 -c "import pwn; print('  ✓ pwntools', pwn.__version__)" 2>/dev/null || echo "  ✗ pwntools (local WSLda bor — serverga shart emas)"
echo "==== TAYYOR ===="
