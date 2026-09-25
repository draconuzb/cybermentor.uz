#!/bin/bash
HOST="37d48d83-8995-41f0-8e11-5e5785248075.red.cyberkent.uz"
echo "---dig---"
dig +short "$HOST"
echo "---curl-verbose-root---"
curl -sv -m 8 "http://$HOST/" 2>&1 | head -60
echo "---preview-loopback---"
curl -s -m 8 -X POST "http://$HOST/api/preview" -H "Content-Type: application/json" -d '{"url":"http://127.0.0.1/"}'
echo
