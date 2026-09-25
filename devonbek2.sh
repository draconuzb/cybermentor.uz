#!/bin/bash
HOST="80db329b-99e8-448f-8872-a1f02c5b1d72.red.cyberkent.uz"
DIR=~/ctf/web/devonbek
cd "$DIR"
JAR=cookies.txt
rm -f "$JAR"
USER="atk_$RANDOM"
PASS="pass123"
echo "user=$USER"

echo "---register page (form fields)---"
curl -s -m 8 "http://$HOST/register" -o reg.html
grep -oE '<input[^>]*>|<form[^>]*>' reg.html

echo "---register POST---"
curl -s -m 8 -c "$JAR" -b "$JAR" -L -X POST "http://$HOST/register" \
  --data-urlencode "username=$USER" --data-urlencode "password=$PASS" -o reg_out.html -w "HTTP:%{http_code}\n"

echo "---cookies after register---"
cat "$JAR"

echo "---dashboard---"
curl -s -m 8 -c "$JAR" -b "$JAR" "http://$HOST/dashboard" -o dash.html -w "HTTP:%{http_code}\n"
wc -c dash.html
cat dash.html
