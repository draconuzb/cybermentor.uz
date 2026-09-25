import re
data = open("qolyozma.pdf", "rb").read()
m = re.search(rb"8 0 obj(.*?)endobj", data, re.S)
print(m.group(1)[:2000])
