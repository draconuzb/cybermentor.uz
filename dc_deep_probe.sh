#!/bin/bash
HOST="4ed50d16-32a2-4240-8072-cf19063a8651.red.cyberkent.uz"
echo "---vpn status---"
~/.local/bin/vpn-status
echo "---dig---"
dig +short "$HOST"
echo "---curl -i root---"
curl -si -m 8 "http://$HOST/" | head -20
echo "---curl https---"
curl -sik -m 8 "https://$HOST/" | head -20
echo "---curl various ports on same host---"
for port in 80 443 8080 8000 8443 21 22 445 139 9000; do
  code=$(curl -s -m 4 -o /dev/null -w "%{http_code}" "http://$HOST:$port/" 2>&1)
  echo "port $port -> $code"
done
echo "---nmap resolved ip if any---"
IP=$(dig +short "$HOST" | tail -1)
echo "resolved IP: $IP"
if [ -n "$IP" ]; then
  sudo nmap -Pn -T4 -p 21,22,80,139,443,445,8000,8080,8443,9000,9411,20199 "$IP" 2>&1 | tail -25
fi
