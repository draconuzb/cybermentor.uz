#!/bin/bash
HOST="6e197819-b3b8-423c-b184-ac91fd95fe81.red.cyberkent.uz"
DIR=~/ctf/web/marosim
cd "$DIR"
JAR=cookies.txt

echo "---ticket page---"
curl -s -m 8 -b "$JAR" -c "$JAR" "http://$HOST/ticket" -o ticket.html -w "HTTP:%{http_code}\n"
cat ticket.html

echo "---admin (as normal user)---"
curl -s -m 8 -b "$JAR" -c "$JAR" "http://$HOST/admin" -o admin.html -w "HTTP:%{http_code}\n"
cat admin.html
