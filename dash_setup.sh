#!/bin/bash
# dash_setup.sh — fail2ban + CyberKent web panel (/dash)
set -u
export DEBIAN_FRONTEND=noninteractive

echo "[1] fail2ban (SSH himoya) + flask + gunicorn..."
sudo apt-get install -y -qq fail2ban python3-flask gunicorn >/dev/null 2>&1
sudo systemctl enable --now fail2ban >/dev/null 2>&1
echo "  fail2ban: $(systemctl is-active fail2ban)  |  flask: $(python3 -c 'import flask;print(flask.__version__)' 2>/dev/null)"

echo "[2] Panel fayllarini joylash..."
mkdir -p ~/panel ~/.panel
cp ~/panel_app.py ~/panel/app.py
[ -f ~/.panel/pass ] || openssl rand -base64 9 > ~/.panel/pass
echo "  Panel PAROL: $(cat ~/.panel/pass)"

echo "[3] systemd xizmat (panel)..."
sudo tee /etc/systemd/system/panel.service >/dev/null <<EOF
[Unit]
Description=CyberKent Red Team Panel
After=network.target
[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/panel
ExecStart=/usr/bin/gunicorn -w 2 -b 127.0.0.1:8090 app:app
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now panel >/dev/null 2>&1
sleep 3
echo "  panel: $(systemctl is-active panel)"

echo "[4] nginx /dash marshruti..."
if ! grep -q 'location /dash' /etc/nginx/conf.d/cybermentor.conf; then
  sudo sed -i '/location \/ {/i\    location /dash/ {\n        proxy_pass http://127.0.0.1:8090/;\n        proxy_set_header Host $host;\n        proxy_set_header X-Forwarded-For $remote_addr;\n        proxy_set_header X-Forwarded-Proto $scheme;\n    }\n' /etc/nginx/conf.d/cybermentor.conf
  sudo nginx -t >/dev/null 2>&1 && sudo systemctl reload nginx && echo "  ✓ /dash yoqildi"
fi

echo "[5] Ichki test..."
curl -sS -m 8 -o /dev/null -w "  local /login -> HTTP %{http_code}\n" http://127.0.0.1:8090/login 2>/dev/null
sudo journalctl -u panel --no-pager -n 4 2>/dev/null | tail -4
echo "======================================================"
echo " PANEL: https://cybermentor.uz/dash/"
echo " PAROL: $(cat ~/.panel/pass)"
echo "======================================================"
