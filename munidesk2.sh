#!/bin/bash
HOST="6579ec46-d42a-4b5a-b860-f4e8d2d3cabe.red.cyberkent.uz"
DIR=~/ctf/web/munitsipal_desk
cd "$DIR"
echo "---register-page---"
curl -s -m 8 "http://$HOST/register" -o register.html
wc -c register.html
grep -oE '<input[^>]*>|<form[^>]*>' register.html
echo "---login-page---"
curl -s -m 8 "http://$HOST/login" -o login.html
grep -oE '<input[^>]*>|<form[^>]*>' login.html
echo "---admin (no auth)---"
curl -s -m 8 -o /dev/null -w "HTTP:%{http_code}\n" "http://$HOST/admin"
