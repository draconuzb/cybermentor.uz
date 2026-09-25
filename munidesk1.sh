#!/bin/bash
HOST="6579ec46-d42a-4b5a-b860-f4e8d2d3cabe.red.cyberkent.uz"
DIR=~/ctf/web/munitsipal_desk
mkdir -p "$DIR"
cd "$DIR"
echo "---root---"
curl -s -m 8 "http://$HOST/" -o root.html
wc -c root.html
echo "---links/forms---"
grep -oE 'href="[^"]+"|action="[^"]+"|src="[^"]+"' root.html | sort -u
