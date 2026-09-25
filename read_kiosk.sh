#!/bin/bash
cd ~/ctf/forensics/kiosk7/mnt
echo ---BOOKMARKS---
cat profile/bookmarks.html
echo
echo ---LOGS---
for f in logs/log_*.txt logs/manifest.log; do
  echo "-- $f --"
  cat "$f"
  echo
done
