#!/bin/bash
HOST="6579ec46-d42a-4b5a-b860-f4e8d2d3cabe.red.cyberkent.uz"
DIR=~/ctf/web/munitsipal_desk
cd "$DIR"
JAR=cookies.txt
rm -f "$JAR"
USER="atk_$RANDOM"
PASS="pass123"
echo "user=$USER"

echo "---register---"
curl -s -m 8 -c "$JAR" -b "$JAR" -L -X POST "http://$HOST/register" \
  --data-urlencode "username=$USER" --data-urlencode "password=$PASS" -o reg_out.html -w "HTTP:%{http_code}\n"

echo "---login---"
curl -s -m 8 -c "$JAR" -b "$JAR" -L -X POST "http://$HOST/login" \
  --data-urlencode "username=$USER" --data-urlencode "password=$PASS" -o login_out.html -w "HTTP:%{http_code}\n"
grep -oiE 'ticket|dashboard|welcome|error|invalid' login_out.html | sort -u

echo "---dashboard/home after login---"
curl -s -m 8 -c "$JAR" -b "$JAR" "http://$HOST/" -o home_out.html
wc -c home_out.html
grep -oE 'href="[^"]+"' home_out.html | sort -u
