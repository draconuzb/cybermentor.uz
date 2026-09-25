#!/bin/bash
cd ~/ctf/forensics/kiosk7/mnt
for f in logs/log_*.txt logs/manifest.log; do
  echo "-- $f (size $(stat -c%s "$f")) --"
  xxd "$f"
  echo
done
