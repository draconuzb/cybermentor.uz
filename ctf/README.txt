=== CYBERKENT CTF — HUJUM BAZASI (cybermentor server) ===

10:00'da red.cyberkent.uz/vpn dan shaxsiy .ovpn'ni yuklab oling.

1) .ovpn ni serverga qo'ying:
   - code-server Explorer'ga drag-drop qiling (~/ ga), yoki
   - nomini cyberkent.ovpn qiling

2) Ulaning:
   vpn-connect ~/cyberkent.ovpn
   -> "ATTACK IP (LHOST) = 10.x.x.x" chiqadi. Shu sizning IP.

3) Foydali buyruqlar:
   vpn-status    -> ulanish holati + IP
   vpn-ip        -> faqat attack IP (reverse shell LHOST)
   vpn-log       -> VPN loglari
   vpn-off       -> uzish

4) Hujum (target IP = panelдan):
   nmap -sVC -T4 <target>
   ffuf -u http://<target>/FUZZ -w ~/wordlists/common.txt
   Reverse shell LHOST = `vpn-ip` natijasi, listener: nc -lvnp 4444

Asboblar: nmap ffuf gobuster sqlmap nikto hydra john hashcat gdb+GEF
radare2 binwalk exiftool steghide zsteg stegseek volatility3(vol) impacket
RsaCtfTool nth ROPgadget one_gadget + CyberChef: /cyberchef/
