#!/bin/bash
for H in "1431-4ed50d16-32a2-4240-8072-cf19063a8651.red.cyberkent.uz" "4ed50d16-32a2-4240-8072-cf19063a8651.red.cyberkent.uz"; do
  echo "=== $H ==="
  dig +short "$H"
  code=$(curl -s -m 6 -o /dev/null -w "%{http_code}" "http://$H/" --resolve "$H:80:10.13.37.10")
  echo "HTTP:$code"
done

echo "--- banner grabs ---"
for p in 9411 20199 21 445 139 8080 8000 9000; do
  out=$(timeout 3 bash -c "exec 3<>/dev/tcp/10.13.37.10/$p; cat <&3" 2>&1 | head -c 200)
  echo "port $p -> ${out:-<no data / closed>}"
done
