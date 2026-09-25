#!/bin/bash
HOST="6e197819-b3b8-423c-b184-ac91fd95fe81.red.cyberkent.uz"
DIR=~/ctf/web/marosim
mkdir -p "$DIR"
cd "$DIR"
echo "---root---"
curl -s -m 8 "http://$HOST/" -o root.html
wc -c root.html
grep -oE 'href="[^"]+"|action="[^"]+"' root.html | sort -u
