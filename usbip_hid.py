import struct

# Parse raw pcapng file manually is complex; instead use tshark to dump raw TCP payload per frame via -T fields -e tcp.payload
import subprocess

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

# Get list of USBIP RET_SUBMIT frames with devid + tcp.payload hex
out = run(
    "tshark -r /tmp/usbip.pcapng -d tcp.port==3240,usbip -Y \"usbip.urb==0x00000003\" "
    "-T fields -e frame.number -e usb.src -e tcp.payload"
)

HID_MAP = {
    0x04: 'a', 0x05: 'b', 0x06: 'c', 0x07: 'd', 0x08: 'e', 0x09: 'f', 0x0a: 'g',
    0x0b: 'h', 0x0c: 'i', 0x0d: 'j', 0x0e: 'k', 0x0f: 'l', 0x10: 'm', 0x11: 'n',
    0x12: 'o', 0x13: 'p', 0x14: 'q', 0x15: 'r', 0x16: 's', 0x17: 't', 0x18: 'u',
    0x19: 'v', 0x1a: 'w', 0x1b: 'x', 0x1c: 'y', 0x1d: 'z',
    0x1e: '1', 0x1f: '2', 0x20: '3', 0x21: '4', 0x22: '5', 0x23: '6', 0x24: '7',
    0x25: '8', 0x26: '9', 0x27: '0',
    0x28: '\n', 0x2c: ' ', 0x2d: '-', 0x2e: '=', 0x33: ';', 0x34: "'",
    0x36: ',', 0x37: '.', 0x38: '/', 0x2f: '[', 0x30: ']', 0x31: '\\',
    0x59: '1', 0x5a: '2', 0x5b: '3', 0x5c: '4', 0x5d: '5',
    0x5e: '6', 0x5f: '7', 0x60: '8', 0x61: '9', 0x62: '0',
}
HID_MAP_SHIFT = {
    0x1e: '!', 0x1f: '@', 0x20: '#', 0x21: '$', 0x22: '%', 0x23: '^', 0x24: '&',
    0x25: '*', 0x26: '(', 0x27: ')', 0x2d: '_', 0x2e: '+', 0x36: '<', 0x37: '>',
    0x38: '?', 0x33: ':', 0x34: '"',
}

streams = {}
last_key = {}
for line in out.strip().splitlines():
    parts = line.split('\t')
    if len(parts) < 3:
        continue
    frame_no, src, payload_hex = parts[0], parts[1], parts[2]
    payload_hex = payload_hex.replace(':', '')
    if not payload_hex:
        continue
    data = bytes.fromhex(payload_hex)
    if len(data) < 48 + 8:
        continue
    hid = data[48:56]
    modifier = hid[0]
    keycode = hid[2]
    if keycode == 0:
        continue
    key = (modifier, keycode)
    prev = last_key.get(src)
    last_key[src] = key
    if key == prev:
        continue
    shift = bool(modifier & 0x22)
    ch = None
    if shift and keycode in HID_MAP_SHIFT:
        ch = HID_MAP_SHIFT[keycode]
    elif keycode in HID_MAP:
        ch = HID_MAP[keycode].upper() if shift and HID_MAP[keycode].isalpha() else HID_MAP[keycode]
    else:
        ch = f"[{keycode:02x}]"
    streams.setdefault(src, []).append(ch)

for src, chars in streams.items():
    text = "".join(chars)
    print(f"=== device {src} ===")
    print(repr(text[:500]))

# debug raw sequence for 1.2.1
print("\n--- raw seq for 1.2.1 ---")
last_key2 = {}
seq = []
for line in out.strip().splitlines():
    parts = line.split('\t')
    if len(parts) < 3:
        continue
    frame_no, src, payload_hex = parts[0], parts[1], parts[2]
    if src != "1.2.1":
        continue
    payload_hex = payload_hex.replace(':', '')
    if not payload_hex:
        continue
    data = bytes.fromhex(payload_hex)
    if len(data) < 56:
        continue
    hid = data[48:56]
    modifier = hid[0]
    keycode = hid[2]
    seq.append((frame_no, modifier, keycode))

for f, m, k in seq[:60]:
    print(f, hex(m), hex(k))
