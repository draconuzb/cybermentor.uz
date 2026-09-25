#!/bin/bash
HOST="4ed50d16-32a2-4240-8072-cf19063a8651.red.cyberkent.uz"
for p in dc.pcap files/dc.pcap download/dc.pcap static/dc.pcap pcap/dc.pcap capture/dc.pcap data/dc.pcap uploads/dc.pcap dc.pcapng files dc pcaps/dc.pcap; do
  code=$(curl -s -m 6 -o /dev/null -w "%{http_code}" "http://$HOST/$p")
  echo "$p -> $code"
done
