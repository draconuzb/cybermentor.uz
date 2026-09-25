#!/bin/bash
for f in 4 88 118 124 178; do
  echo "== frame $f =="
  tshark -r /tmp/tls.pcap -Y "frame.number==$f" -V 2>&1 | grep "ALPN Next Protocol"
done
