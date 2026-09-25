#!/bin/bash
cd ~/ctf/forensics/kiosk7
for i in 0 1 2 3 4 5; do
  echo "== log_$i =="
  grep -abo "kiosk7 session log segment $i" kiosk7.img
done
echo "== manifest =="
grep -abo "kiosk7 log manifest" kiosk7.img
