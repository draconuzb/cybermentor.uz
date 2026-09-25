#!/bin/bash
# attack_pack.sh — HTB/OffSec uslubidagi qo'shimcha hujum asboblari
set -u
export DEBIAN_FRONTEND=noninteractive
export PATH="$HOME/.local/bin:$PATH"
echo "==== ATTACK PACK ===="

echo "[1] nuclei (vuln scanner)..."
if ! command -v nuclei >/dev/null 2>&1; then
  U=$(curl -fsSL https://api.github.com/repos/projectdiscovery/nuclei/releases/latest | grep browser_download_url | grep -oE 'https[^"]+linux_amd64\.zip' | head -1)
  curl -fsSL -o /tmp/nuclei.zip "$U" 2>/dev/null && sudo unzip -oq /tmp/nuclei.zip -d /usr/local/bin nuclei && sudo chmod +x /usr/local/bin/nuclei && echo "  ✓ $(nuclei -version 2>&1 | head -1)" || echo "  ✗ nuclei"
fi

echo "[2] feroxbuster..."
if ! command -v feroxbuster >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/epi052/feroxbuster/main/install-nix.sh 2>/dev/null | sudo bash -s -- /usr/local/bin >/dev/null 2>&1 && echo "  ✓ feroxbuster" || echo "  ✗ feroxbuster"
fi

echo "[3] gemlar: evil-winrm, wpscan..."
sudo gem install evil-winrm wpscan >/dev/null 2>&1 && echo "  ✓ evil-winrm + wpscan" || echo "  ✗ gem (biri tushmadi)"

echo "[4] pipx: netexec, smbmap, enum4linux-ng..."
pipx install netexec >/dev/null 2>&1 && echo "  ✓ netexec (nxc)" || echo "  ✗ netexec"
pipx install smbmap >/dev/null 2>&1 && echo "  ✓ smbmap" || python3 -m pip install --break-system-packages -q smbmap 2>/dev/null && echo "  ✓ smbmap(pip)"
pipx install enum4linux-ng >/dev/null 2>&1 && echo "  ✓ enum4linux-ng" || echo "  ✗ enum4linux-ng"

echo "[5] searchsploit (exploit-db, katta ~1GB — sabr)..."
if [ ! -d /opt/exploitdb ]; then
  sudo git clone --depth 1 -q https://gitlab.com/exploit-database/exploitdb /opt/exploitdb 2>/dev/null && sudo ln -sf /opt/exploitdb/searchsploit /usr/local/bin/searchsploit && echo "  ✓ searchsploit" || echo "  ✗ searchsploit"
fi

echo
echo "==== TEKSHIRUV ===="
for t in nuclei feroxbuster evil-winrm wpscan nxc netexec smbmap enum4linux-ng searchsploit; do
  command -v "$t" >/dev/null 2>&1 && printf "  ✓ %s\n" "$t" || printf "  ✗ %s\n" "$t"
done
echo "==== TAYYOR ===="
