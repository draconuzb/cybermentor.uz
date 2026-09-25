#!/bin/bash
export PATH="$HOME/.local/bin:/usr/local/bin:$PATH"
D=/tmp/webdemo; rm -rf "$D"; mkdir -p "$D/admin"
printf '<h1>CyberKent Demo Bank</h1>\n<a href="/login.php">Login</a>\n' > "$D/index.html"
printf 'User-agent: *\nDisallow: /admin/\n' > "$D/robots.txt"
printf 'CYBERKENT{ffuf_bilan_yashirin_panel_topildi_2026}\n' > "$D/admin/flag.txt"
printf '<h1>Login</h1><form>...</form>\n' > "$D/login.php"
cd "$D"
python3 -m http.server 9000 --bind 127.0.0.1 >/tmp/web.log 2>&1 &
SV=$!; sleep 2

echo "########## MINI WEB CHALLENGE: http://127.0.0.1:9000 ##########"
echo "(xuddi CyberKent web-challenge'idek — maqsad: flag topish)"
echo
echo "==== 1-QADAM: robots.txt ni tekshiraman (ko'p CTF'da hiyla shu yerda) ===="
curl -s http://127.0.0.1:9000/robots.txt
echo "   >>> 'Disallow: /admin/' — demak /admin qiziq!"
echo
echo "==== 2-QADAM: ffuf bilan yashirin papkalarni skanlayman ===="
ffuf -u http://127.0.0.1:9000/FUZZ -w ~/wordlists/common.txt -mc 200,301,302,403 -t 60 -s 2>/dev/null | sort -u | head
echo "   >>> 'admin' topildi ✓"
echo
echo "==== 3-QADAM: /admin/ ichiga qarayman ===="
curl -s http://127.0.0.1:9000/admin/ | grep -oE 'href="[^"]+"' | head
echo "   >>> flag.txt ko'rinyapti!"
echo
echo "==== 4-QADAM: FLAG'ni olaman ===="
echo -n "   FLAG = "; curl -s http://127.0.0.1:9000/admin/flag.txt
echo
echo "########## challenge YECHILDI ##########"
kill $SV 2>/dev/null
