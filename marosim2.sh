#!/bin/bash
HOST="6e197819-b3b8-423c-b184-ac91fd95fe81.red.cyberkent.uz"
DIR=~/ctf/web/marosim
cd "$DIR"
JAR=cookies.txt
rm -f "$JAR"
USER="atk_$RANDOM"
PASS="pass123"
echo "user=$USER"

echo "---register page fields---"
curl -s -m 8 "http://$HOST/register" -o reg.html
grep -oE '<input[^>]*>|<form[^>]*>' reg.html

echo "---register POST---"
curl -s -m 8 -c "$JAR" -b "$JAR" -L -X POST "http://$HOST/register" \
  --data-urlencode "username=$USER" --data-urlencode "password=$PASS" -o reg_out.html -w "HTTP:%{http_code}\n"

echo "---login POST (in case register doesn't auto-login)---"
curl -s -m 8 -c "$JAR" -b "$JAR" -L -X POST "http://$HOST/login" \
  --data-urlencode "username=$USER" --data-urlencode "password=$PASS" -o login_out.html -w "HTTP:%{http_code}\n"

echo "---home after login---"
curl -s -m 8 -c "$JAR" -b "$JAR" "http://$HOST/" -o home.html
grep -oE 'href="[^"]+"|action="[^"]+"' home.html | sort -u
echo "---cookies---"
cat "$JAR"
