#!/bin/bash
# ctf_categories.sh — 5 kategoriyaga to'liq moslik
set -u
export DEBIAN_FRONTEND=noninteractive
export PATH="$HOME/.local/bin:$PATH"
echo "==== KATEGORIYA BO'SHLIQLARINI TO'LDIRISH ===="

echo "[PWN] pwntools (unicorn'siz, --no-deps usuli)..."
python3 -m pip install --break-system-packages -q paramiko mako pyelftools capstone ropgadget pysocks python-dateutil requests rpyc intervaltree sortedcontainers unix-ar colored-traceback pyserial packaging zstandard psutil six 2>&1 | tail -1
python3 -m pip install --break-system-packages -q --no-deps pwntools 2>&1 | tail -1
python3 -c "from pwn import *; print('  ✓ pwntools:', pwnlib.__version__)" 2>&1 | tail -1

echo "[CRYPTO] pycryptodome, gmpy2, sympy, factordb..."
sudo apt-get install -y -qq python3-gmpy2 python3-sympy >/dev/null 2>&1
python3 -m pip install --break-system-packages -q pycryptodome factordb-pycli 2>&1 | tail -1
python3 -c "import Crypto,gmpy2,sympy; print('  ✓ crypto libs')" 2>&1 | tail -1

echo "[TARMOQ] tcpdump, termshark..."
sudo apt-get install -y -qq tcpdump termshark >/dev/null 2>&1
for t in tcpdump tshark termshark; do command -v $t >/dev/null && echo "  ✓ $t" || echo "  ✗ $t"; done

echo "[STEGO] outguess, stegolsb, exiftool, pngcheck..."
sudo apt-get install -y -qq outguess >/dev/null 2>&1
python3 -m pip install --break-system-packages -q stegolsb 2>/dev/null
for t in outguess zsteg stegseek steghide binwalk exiftool zbarimg; do command -v $t >/dev/null && echo "  ✓ $t" || echo "  ✗ $t"; done

echo
echo "======================================================"
echo " 5 KATEGORIYA — MOSLIK HISOBOTI"
echo "======================================================"
chk() { command -v "$1" >/dev/null 2>&1 && printf "✓" || printf "✗"; }
echo "WEB:      ffuf$(chk ffuf) gobuster$(chk gobuster) feroxbuster$(chk feroxbuster) sqlmap$(chk sqlmap) nuclei$(chk nuclei) nikto$(chk nikto) wpscan$(chk wpscan) whatweb$(chk whatweb)"
echo "PWN:      gdb$(chk gdb) radare2$(chk radare2) ROPgadget$(chk ROPgadget) one_gadget$(chk one_gadget) checksec$(chk checksec) nasm$(chk nasm) $(python3 -c 'import pwn' 2>/dev/null && echo pwntools✓ || echo pwntools✗)"
echo "CRYPTO:   RsaCtfTool$(chk RsaCtfTool) hashcat$(chk hashcat) john$(chk john) openssl$(chk openssl) $(python3 -c 'import Crypto' 2>/dev/null && echo pycryptodome✓ || echo pycryptodome✗) nth$(chk nth)"
echo "TARMOQ:   tshark$(chk tshark) tcpdump$(chk tcpdump) termshark$(chk termshark) nmap$(chk nmap) wireshark-cli"
echo "STEGO:    steghide$(chk steghide) zsteg$(chk zsteg) stegseek$(chk stegseek) binwalk$(chk binwalk) exiftool$(chk exiftool) foremost$(chk foremost) outguess$(chk outguess) zbarimg$(chk zbarimg)"
echo "+ CyberChef (web), PayloadsAllTheThings, searchsploit$(chk searchsploit)"
echo "==== TAYYOR ===="
