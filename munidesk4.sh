#!/bin/bash
HOST="6579ec46-d42a-4b5a-b860-f4e8d2d3cabe.red.cyberkent.uz"
for i in 1 2 3 4 5; do
  code=$(curl -s -m 5 -o /dev/null -w "%{http_code}" "http://$HOST/")
  echo "attempt $i -> HTTP $code"
  sleep 1
done
