#!/bin/bash
BASE="http://4ed50d16-32a2-4240-8072-cf19063a8651.red.cyberkent.uz"
for p in "" dc.pcap capture.pcap traffic.pcap file.pcap dc.pcapng download files static robots.txt; do
  code=$(curl -s -o /dev/null -m 10 -w "%{http_code}" "$BASE/$p")
  echo "$p -> $code"
done
