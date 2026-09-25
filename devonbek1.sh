#!/bin/bash
HOST="80db329b-99e8-448f-8872-a1f02c5b1d72.red.cyberkent.uz"
DIR=~/ctf/web/devonbek
mkdir -p "$DIR"
cd "$DIR"
echo "---root---"
curl -s -m 8 "http://$HOST/" -o root.html
wc -c root.html
grep -oE 'href="[^"]+"|action="[^"]+"' root.html | sort -u
