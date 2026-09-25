#!/bin/bash
cd ~/ctf/forensics/kiosk7
CLUSTER=2048
starts=(139264 141312 143360 145408 147456 149504 151552)
names=(log_0 log_1 log_2 log_3 log_4 log_5 manifest)
for i in "${!starts[@]}"; do
  cstart=${starts[$i]}
  name=${names[$i]}
  fsize=50
  if [ "$name" == "manifest" ]; then fsize=28; fi
  slack_off=$((cstart + fsize))
  slack_len=$((CLUSTER - fsize))
  echo "== $name slack: offset=$slack_off len=$slack_len =="
  dd if=kiosk7.img bs=1 skip=$slack_off count=$slack_len 2>/dev/null | strings -n 4
  echo "--hex head--"
  dd if=kiosk7.img bs=1 skip=$slack_off count=64 2>/dev/null | xxd
done
