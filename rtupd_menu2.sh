#!/bin/bash
opt=$1
exec 3<>/dev/tcp/10.13.37.10/21612
echo "$opt" >&3
sleep 1
timeout 3 cat <&3
