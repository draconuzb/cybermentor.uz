#!/bin/bash
# ctf_tools.sh — cybermentor.uz serveriga CTF asboblari + Claude Code o'rnatish
set -u
export DEBIAN_FRONTEND=noninteractive
echo "==== CTF ASBOBLAR O'RNATISH ===="

echo "[1] apt paketlar (bittalab, xato bo'lsa o'tkazib yuboradi)..."
sudo apt-get update -qq
for p in nmap sqlmap nikto hydra john binwalk foremost steghide exiftool netcat-openbsd whatweb gobuster ffuf dirb python3-pip pipx ruby-full build-essential unzip p7zip-full; do
  sudo apt-get install -y -qq "$p" >/dev/null 2>&1 && echo "  ✓ $p" || echo "  ✗ $p (yoq)"
done

echo "[2] pip asboblar (pwntools, impacket)..."
pipx ensurepath >/dev/null 2>&1 || true
python3 -m pip install --user --quiet --break-system-packages pwntools impacket 2>/dev/null && echo "  ✓ pwntools + impacket" || echo "  ✗ pip (keyin qayta)"

echo "[3] wordlist (rockyou)..."
mkdir -p ~/wordlists
[ -f ~/wordlists/rockyou.txt ] || curl -fsSL -o ~/wordlists/rockyou.txt https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt 2>/dev/null && echo "  ✓ rockyou: $(wc -l < ~/wordlists/rockyou.txt 2>/dev/null) parol"

echo "[4] Claude Code o'rnatish..."
if ! command -v claude >/dev/null 2>&1; then
  curl -fsSL https://claude.com/install.sh | bash 2>&1 | tail -2
fi
export PATH="$HOME/.local/bin:$PATH"
grep -q '.local/bin' ~/.bashrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
command -v claude && claude --version 2>/dev/null && echo "  ✓ Claude Code (login keyin: 'claude')" || echo "  ✗ claude PATH tekshir"

echo "[5] CTF ish-papka..."
mkdir -p ~/ctf/{web,crypto,forensics,rev,pwn,stego,misc}
echo "  ✓ ~/ctf/ tayyor"

echo
echo "==== TEKSHIRUV ===="
for t in nmap sqlmap nikto hydra john binwalk exiftool steghide gobuster ffuf whatweb claude; do
  command -v "$t" >/dev/null 2>&1 && echo "  ✓ $t" || echo "  ✗ $t"
done
echo "==== BAJARILDI ===="
