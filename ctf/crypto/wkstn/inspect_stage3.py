import json

d = json.load(open("stage3.json"))
for k, v in d.items():
    if isinstance(v, str) and len(v) > 200:
        print(k, type(v), len(v))
    else:
        print(k, ":", v)
