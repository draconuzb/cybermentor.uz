#!/bin/bash
HOST="4ed50d16-32a2-4240-8072-cf19063a8651.red.cyberkent.uz"
mkdir -p ~/ctf/network/domen_qorovuli3
cd ~/ctf/network/domen_qorovuli3
echo "---root---"
curl -s -m 10 "http://$HOST/" -o root.html
wc -c root.html
echo "---links---"
grep -oE 'href="[^"]+"|src="[^"]+"' root.html | sort -u
