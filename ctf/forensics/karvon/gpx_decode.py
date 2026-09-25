import re

data = open("track_main.gpx", encoding="utf-8").read()
wpts = re.findall(r'<wpt lat="([\d.]+)" lon="([\d.]+)"><name>(CP\d+)</name>', data)

chars = []
for lat, lon, name in wpts:
    frac = lat.split(".")[1]
    last3 = int(frac[-3:])
    chars.append(chr(last3))

msg = "".join(chars)
print("lat-based:", msg)

chars2 = []
for lat, lon, name in wpts:
    frac = lon.split(".")[1]
    last3 = int(frac[-3:])
    chars2.append(chr(last3))
print("lon-based:", "".join(chars2))
