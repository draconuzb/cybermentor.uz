#!/bin/bash
BASE="http://8a086c8c-5f4a-4125-b5ff-196cd645b8ce.red.cyberkent.uz"
mkdir -p /tmp/cb_js
for f in 011j8zku8l9-n.js 09k7m7wq4aqaz.js 0cz1d0mv5g_q7.js 0xc04rdb9scva.js 10uw6lr12pgvb.js 2yd39cvd6i2zf.js 32gnwjb_d4dyi.js 3qdnukccxym7v.js turbopack-2a-facqfr25k6.js; do
  curl -s --max-time 10 -o "/tmp/cb_js/$f" "$BASE/_next/static/chunks/$f"
done
echo "=== /api/ references ==="
grep -oE '/api/[a-zA-Z0-9/_-]*' /tmp/cb_js/*.js | sort -u
echo "=== other interesting keywords ==="
grep -oE '"(analytics|internal|admin|superuser|proxy|fetch|ssrf)[a-zA-Z0-9/_-]*"' /tmp/cb_js/*.js | sort -u | head -60
