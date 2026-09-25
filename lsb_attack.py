import socket
import sys
from fractions import Fraction
import time

HOST = "10.13.37.10"
PORT = 21869

N = 87323025951104298572180514013172030932258504490160119967725916489623763238457355641039166198614372003800260626972841865043178840163839374773558148983631352993385742572310795019013257775333984412906784233125895419437040448746356823021529406517888176058790587185730774354888981179608307326979352885674277118207
E = 65537
C = 76568061868019447437663301775225061738251422097668873860795670707629420453842466312683299524441807923140386201460794337488110976581617390504254269999868954038627257128536658673753221990011911383626330608350588926642792559781418641825679953418097729315464679485051541754925935270686057511112114365596359424384

s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(1.5)
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
except socket.timeout:
    pass
s.settimeout(10)

buf = b""

def readline():
    global buf
    while b"\n" not in buf:
        chunk = s.recv(4096)
        if not chunk:
            raise RuntimeError("connection closed")
        buf += chunk
    line, buf2 = buf.split(b"\n", 1)
    buf = buf2
    return line

def oracle(cval):
    s.sendall(f"ORACLE {cval}\n".encode())
    line = readline()
    return int(line.strip())

nbits = N.bit_length()
print("N bits:", nbits, file=sys.stderr)

f = pow(2, E, N)
c = C
lo = Fraction(0)
hi = Fraction(N)

t0 = time.time()
for i in range(nbits):
    c = (c * f) % N
    bit = oracle(c)
    mid = (lo + hi) / 2
    if bit == 0:
        hi = mid
    else:
        lo = mid
    if i % 100 == 0:
        print(f"iter {i}/{nbits} elapsed {time.time()-t0:.1f}s", file=sys.stderr)

m = int(hi)
print("candidate m (int(hi)):", file=sys.stderr)

for cand in [int(hi), int(hi) + 1, int(lo), int(lo) + 1]:
    if pow(cand, E, N) == C:
        mb = cand.to_bytes((cand.bit_length() + 7) // 8, 'big')
        print("VERIFIED plaintext:", mb)
        s.close()
        sys.exit(0)

print("no candidate verified; hi=", hi, "lo=", lo)
s.close()
