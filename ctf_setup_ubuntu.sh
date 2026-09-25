#!/bin/bash
# ctf_setup_ubuntu.sh — cybermentor.uz CTF platformasi (Ubuntu 26.04, code-server + nginx)
set -u
export DEBIAN_FRONTEND=noninteractive
echo "======================================================"
echo " CYBERMENTOR.UZ — CTF PLATFORMA O'RNATISH"
echo "======================================================"

echo "[1/6] apt update + asosiy paketlar..."
sudo apt-get update -qq
sudo apt-get install -y -qq nginx curl git unzip jq ufw 2>&1 | tail -1
echo "     OK"

echo "[2/6] code-server o'rnatish..."
if ! command -v code-server >/dev/null 2>&1; then
  curl -fsSL https://code-server.dev/install.sh | sh 2>&1 | tail -2
fi
code-server --version | head -1

echo "[3/6] code-server sozlash (parol)..."
mkdir -p ~/.config/code-server
PASS=$(openssl rand -base64 12)
cat > ~/.config/code-server/config.yaml <<EOF
bind-addr: 127.0.0.1:8080
auth: password
password: $PASS
cert: false
EOF
sudo systemctl enable --now code-server@ubuntu
sleep 3
echo "     code-server:" $(systemctl is-active code-server@ubuntu)

echo "[4/6] nginx reverse-proxy (cybermentor.uz)..."
sudo rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true
sudo tee /etc/nginx/conf.d/cybermentor.conf >/dev/null <<'NGINX'
server {
    listen 80;
    listen [::]:80;
    server_name cybermentor.uz www.cybermentor.uz;
    client_max_body_size 512m;
    location / {
        proxy_pass http://127.0.0.1:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
NGINX
sudo nginx -t && sudo systemctl restart nginx && echo "     nginx OK"

echo "[5/6] Firewall (ufw)..."
sudo ufw allow 22/tcp >/dev/null 2>&1 || true
sudo ufw allow 80/tcp >/dev/null 2>&1 || true
sudo ufw allow 443/tcp >/dev/null 2>&1 || true
echo "     portlar 22/80/443 ochiq"

echo "[6/6] Holat..."
echo "     tinglayotgan portlar:"
sudo ss -ltnp 2>/dev/null | grep -E ':80|:8080' || true

echo
echo "======================================================"
echo " TAYYOR!"
echo " code-server PAROL:  $PASS"
echo "======================================================"
echo " Test (IP orqali): http://52.91.141.253  (AWS SG'da 80-port ochiq bo'lsa)"
echo " Keyingi: Cloudflare A record cybermentor.uz -> 52.91.141.253"
