#!/bin/bash
HOST="6e197819-b3b8-423c-b184-ac91fd95fe81.red.cyberkent.uz"
DIR=~/ctf/web/marosim
cd "$DIR"
JAR=cookies.txt

echo "---attachment endpoint (headers+body)---"
curl -si -m 8 -b "$JAR" -c "$JAR" "http://$HOST/ticket/4/attachment"

echo
echo "---whoami---"
curl -s -m 8 -b "$JAR" -c "$JAR" "http://$HOST/whoami"
echo
echo "---queue---"
curl -s -m 8 -b "$JAR" -c "$JAR" "http://$HOST/queue" -w "\nHTTP:%{http_code}\n"
