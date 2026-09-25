#!/bin/bash
for f in 18 19 20 21 22 23 24 25; do
  echo "== frame $f =="
  tshark -r /tmp/ot.pcap -Y "frame.number==$f" -T fields -e data.data
done
