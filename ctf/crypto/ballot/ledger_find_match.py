import json

with open("stage3_ledger.json") as f:
    data = json.load(f)

records = data["ledger"]
redacted = [r for r in records if r["value"] == "REDACTED"][0]
target_c1 = redacted["c1"]

matches = [r for r in records if r["c1"] == target_c1 and r["value"] != "REDACTED"]
print("num matches with same c1:", len(matches))
for m in matches[:3]:
    print(m["value"][:80])

p = int(data["p"])
c2_target = int(redacted["c2"])

if matches:
    m1_val = int(matches[0]["value"])
    c2_1 = int(matches[0]["c2"])
    m2 = (m1_val * c2_target * pow(c2_1, -1, p)) % p
    mb = m2.to_bytes((m2.bit_length() + 7) // 8, 'big')
    print("recovered:", mb)
