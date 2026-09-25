#!/bin/bash
# ctf_extra.sh — cybermentor.uz ga qo'shimcha CTF quvvati
set -u
export DEBIAN_FRONTEND=noninteractive
echo "==== QO'SHIMCHA ASBOBLAR ===="

echo "[1] apt paketlar..."
echo "wireshark-common wireshark-common/install-setuid boolean false" | sudo debconf-set-selections
for p in hashcat wfuzz pngcheck zbar-tools tesseract-ocr tshark python3-unicorn python3-pil sagemath-common qrencode; do
  sudo apt-get install -y -qq "$p" >/dev/null 2>&1 && echo "  ✓ $p" || echo "  ✗ $p (yoq)"
done

echo "[2] Ruby gemlar (zsteg, one_gadget)..."
sudo gem install zsteg one_gadget >/dev/null 2>&1 && echo "  ✓ zsteg + one_gadget" || echo "  ✗ gem"

echo "[3] pip: volatility3, name-that-hash, ROPgadget, pwntools..."
python3 -m pip install --break-system-packages -q volatility3 name-that-hash ROPgadget 2>&1 | tail -1
python3 -m pip install --break-system-packages -q pwntools 2>&1 | tail -1
python3 -c "import pwn; print('  ✓ pwntools', pwn.__version__)" 2>/dev/null || echo "  ✗ pwntools (unicorn hali)"

echo "[4] stegseek (.deb, steghide tez buzish)..."
if ! command -v stegseek >/dev/null 2>&1; then
  curl -fsSL -o /tmp/stegseek.deb https://github.com/RickdeJager/stegseek/releases/download/v0.6/stegseek_0.6-1.deb 2>/dev/null && sudo dpkg -i /tmp/stegseek.deb >/dev/null 2>&1 && echo "  ✓ stegseek" || echo "  ✗ stegseek"
fi

echo "[5] RsaCtfTool (crypto RSA)..."
if [ ! -d ~/tools/RsaCtfTool ]; then
  mkdir -p ~/tools && cd ~/tools
  curl -fsSL -o rsa.tar.gz https://codeload.github.com/RsaCtfTool/RsaCtfTool/tar.gz/refs/heads/master 2>/dev/null && tar xzf rsa.tar.gz && mv RsaCtfTool-master RsaCtfTool && rm rsa.tar.gz
  cd ~/tools/RsaCtfTool && python3 -m pip install --break-system-packages -q . >/dev/null 2>&1 && echo "  ✓ RsaCtfTool" || echo "  ✗ RsaCtfTool"
fi

echo "[6] CyberChef (brauzerda, offline swiss-knife)..."
sudo mkdir -p /var/www/cyberchef
if [ ! -f /var/www/cyberchef/index.html ]; then
  CJ=$(curl -fsSL https://api.github.com/repos/gchq/CyberChef/releases/latest | grep browser_download_url | grep -oE 'https[^"]+\.zip' | head -1)
  curl -fsSL -o /tmp/cc.zip "$CJ" 2>/dev/null && sudo unzip -oq /tmp/cc.zip -d /var/www/cyberchef && sudo bash -c 'f=$(ls /var/www/cyberchef/CyberChef*.html 2>/dev/null | head -1); [ -n "$f" ] && ln -sf "$f" /var/www/cyberchef/index.html' && echo "  ✓ CyberChef -> /var/www/cyberchef"
fi
# nginx location qo'shish (agar yo'q bo'lsa)
if ! grep -q 'location /cyberchef' /etc/nginx/conf.d/cybermentor.conf; then
  sudo sed -i '/location \/ {/i\    location /cyberchef/ {\n        alias /var/www/cyberchef/;\n        index index.html;\n    }\n' /etc/nginx/conf.d/cybermentor.conf
  sudo nginx -t >/dev/null 2>&1 && sudo systemctl reload nginx && echo "  ✓ nginx: /cyberchef yoqildi"
fi

echo
echo "==== YANGI ASBOBLAR TEKSHIRUV ===="
for t in hashcat wfuzz zsteg stegseek volatility3 vol nth ROPgadget one_gadget tshark zbarimg tesseract qrencode; do
  command -v "$t" >/dev/null 2>&1 && printf "  ✓ %s\n" "$t" || printf "  ✗ %s\n" "$t"
done
python3 -c "import pwn" 2>/dev/null && echo "  ✓ pwntools(py)" || echo "  ✗ pwntools(py)"
[ -f /var/www/cyberchef/index.html ] && echo "  ✓ CyberChef: https://cybermentor.uz/cyberchef/"
echo "==== TAYYOR ===="
