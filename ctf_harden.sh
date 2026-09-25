#!/bin/bash
# ctf_harden.sh — cybermentor.uz serverini jangga shay qilish: swap + wordlistlar + tekshiruv
set -u
export DEBIAN_FRONTEND=noninteractive
echo "==== SHAY QILISH ===="

echo "[1] Swap (2GB) — RAM tor, OOM bo'lmasin..."
if ! sudo swapon --show | grep -q swapfile; then
  sudo fallocate -l 2G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile >/dev/null
  sudo swapon /swapfile
  grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
  echo "  ✓ swap yoqildi"
else
  echo "  ✓ swap allaqachon bor"
fi
free -h | grep -E 'Mem|Swap'

echo "[2] SecLists wordlistlar..."
if sudo apt-get install -y -qq seclists >/dev/null 2>&1; then
  echo "  ✓ seclists (apt) -> /usr/share/seclists"
else
  mkdir -p ~/wordlists
  curl -fsSL -o ~/wordlists/directory-list-2.3-medium.txt https://raw.githubusercontent.com/3ndG4me/KaliLists/master/dirbuster/directory-list-2.3-medium.txt 2>/dev/null && echo "  ✓ directory-list-medium: $(wc -l < ~/wordlists/directory-list-2.3-medium.txt) qator"
  curl -fsSL -o ~/wordlists/common.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt 2>/dev/null && echo "  ✓ common.txt: $(wc -l < ~/wordlists/common.txt) qator"
fi

echo "[3] Foydali qo'shimchalar (jq, dnsutils, seclists uchun)..."
for p in dnsutils whois wget tmux ripgrep; do
  sudo apt-get install -y -qq "$p" >/dev/null 2>&1 && echo "  ✓ $p" || echo "  ✗ $p"
done

echo
echo "==== YAKUNIY HOLAT ===="
echo "-- Xizmatlar:"
echo "   code-server: $(systemctl is-active code-server@ubuntu)"
echo "   nginx:       $(systemctl is-active nginx)"
echo "-- Asboblar:"
for t in nmap ffuf gobuster sqlmap nikto hydra john binwalk exiftool steghide whatweb radare2 gdb claude; do
  command -v "$t" >/dev/null 2>&1 && printf "   ✓ %s\n" "$t" || printf "   ✗ %s\n" "$t"
done
echo "-- Wordlistlar:"; ls -1 ~/wordlists/ 2>/dev/null | sed 's/^/   /'; ls /usr/share/seclists >/dev/null 2>&1 && echo "   + /usr/share/seclists"
echo "-- RAM/Swap:"; free -h | grep -E 'Mem|Swap' | sed 's/^/   /'
echo "-- Disk:"; df -h / | tail -1 | sed 's/^/   /'
echo "==== SHAY! ===="
