#!/bin/bash
exec 3<>/dev/tcp/10.13.37.10/21093
{
  echo "PEEK 64"
  sleep 1
  echo "PEEK 128"
  sleep 1
  echo "PEEK 256"
  sleep 1
  echo "EXIT"
  sleep 1
} >&3
timeout 8 cat <&3
