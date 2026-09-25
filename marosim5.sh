#!/bin/bash
HOST="6e197819-b3b8-423c-b184-ac91fd95fe81.red.cyberkent.uz"
DIR=~/ctf/web/marosim
cd "$DIR"
JAR=cookies.txt

echo "---home (ticket list)---"
curl -s -m 8 -b "$JAR" -c "$JAR" "http://$HOST/" -o home2.html
cat home2.html

echo "---ticket/4 view---"
curl -s -m 8 -b "$JAR" -c "$JAR" "http://$HOST/ticket/4" -o t4.html -w "HTTP:%{http_code}\n"
cat t4.html
