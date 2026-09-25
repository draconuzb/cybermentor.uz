import json

with open("stage3_ledger.json") as f:
    data = json.load(f)

print("top-level keys:", list(data.keys()))
for k in data:
    if k not in ("p", "g", "y"):
        v = data[k]
        print(k, type(v), len(v) if hasattr(v, "__len__") else v)

records = data.get("records") or data.get("ledger") or data.get("entries")
if records is None:
    # try to find a list value
    for k, v in data.items():
        if isinstance(v, list):
            records = v
            print("using list key:", k)
            break

print("num records:", len(records))
print("sample record[0]:", records[0])
print("sample record[1]:", records[1])

redacted = [r for r in records if "REDACTED" in json.dumps(r).upper()]
print("num redacted:", len(redacted))
for r in redacted[:3]:
    print("REDACTED entry:", r)
