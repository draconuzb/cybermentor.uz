#!/bin/bash
exec 3<>/dev/tcp/10.13.37.10/21093
{
  echo "HELP"
  sleep 0.5
  echo "PEEK 512"
  sleep 0.5
  echo "PEEK 4096"
  sleep 0.5
  echo "PEEK -1"
  sleep 0.5
  echo "PEEK 99999999"
  sleep 0.5
  echo "EXIT"
  sleep 0.5
} >&3
timeout 10 cat <&3
