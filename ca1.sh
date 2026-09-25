#!/bin/bash
HOST="8c7afcae-f925-4883-a01d-a4952cf05db2.red.cyberkent.uz"
echo "---root---"
curl -s -m 8 "http://$HOST/" -o /tmp/ca_root.html
wc -c /tmp/ca_root.html
echo "---links---"
grep -oE 'href="[^"]+"|src="[^"]+"' /tmp/ca_root.html | sort -u
echo "---stream1---"
curl -s -m 8 "http://$HOST/stream1.txt" -o /tmp/stream1.txt
wc -c /tmp/stream1.txt
head -c 500 /tmp/stream1.txt
echo
