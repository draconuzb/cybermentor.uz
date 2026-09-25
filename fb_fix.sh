#!/bin/bash
# fb_fix.sh — filebrowser binary'ni to'g'ri o'rnatish
set -u
echo "[1] Binary yuklab olish (github release)..."
cd /tmp
curl -fsSL -o fb.tar.gz https://github.com/filebrowser/filebrowser/releases/latest/download/linux-amd64-filebrowser.tar.gz 2>/dev/null
tar xzf fb.tar.gz filebrowser 2>/dev/null
sudo mv -f filebrowser /usr/local/bin/filebrowser
sudo chmod +x /usr/local/bin/filebrowser
echo "  version: $(/usr/local/bin/filebrowser version 2>/dev/null | head -1)"

echo "[2] Config (baseurl /files, root=home, 127.0.0.1:8081)..."
DB="$HOME/filebrowser.db"
rm -f "$DB"
/usr/local/bin/filebrowser config init --database "$DB" >/dev/null 2>&1
/usr/local/bin/filebrowser config set --address 127.0.0.1 --port 8081 --baseurl /files --root "$HOME" --database "$DB" >/dev/null 2>&1
FBPASS=$(cat "$HOME/.fb_pass" 2>/dev/null); [ -z "$FBPASS" ] && FBPASS=$(openssl rand -base64 9) && echo "$FBPASS" > "$HOME/.fb_pass"
/usr/local/bin/filebrowser users add admin "$FBPASS" --perm.admin --database "$DB" >/dev/null 2>&1
echo "  parol: $FBPASS"

echo "[3] Xizmatni qayta ishga tushirish..."
sudo systemctl reset-failed filebrowser 2>/dev/null
sudo systemctl restart filebrowser
sleep 3
echo "  filebrowser: $(systemctl is-active filebrowser)"
echo "  tinglayapti: $(sudo ss -ltnp 2>/dev/null | grep 8081 | head -1)"

echo "[4] Ichki test (localhost /files)..."
curl -sS -m 8 -o /dev/null -w "  local /files -> HTTP %{http_code}\n" http://127.0.0.1:8081/files/ 2>/dev/null
echo "==== filebrowser: https://cybermentor.uz/files/  (admin / $FBPASS) ===="
