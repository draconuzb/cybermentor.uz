#!/bin/bash
export PATH="$HOME/.local/bin:/usr/local/bin:$PATH"
T="http://testphp.vulnweb.com"

echo "############ WEB CHALLENGE DEMO: $T ############"
echo
echo "==== 1. WHATWEB (qanday sayt, texnologiyalar) ===="
whatweb -q "$T" 2>/dev/null

echo
echo "==== 2. FFUF (yashirin sahifa va papkalar) ===="
ffuf -u "$T/FUZZ" -w ~/wordlists/common.txt -mc 200,301,302,403 -t 50 -s 2>/dev/null | head -20

echo
echo "==== 3. SQLMAP (login/parametrда SQL injection bormi) ===="
sqlmap -u "$T/listproducts.php?cat=1" --batch --level=1 --risk=1 2>&1 | grep -iE "is vulnerable|injectable|Parameter:|Type:|Title:|payload:|back-end DBMS" | head -14
echo
echo "############ DEMO TUGADI ############"
