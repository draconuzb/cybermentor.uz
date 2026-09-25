#!/bin/bash
set -u
export DEBIAN_FRONTEND=noninteractive
export PATH="$HOME/.local/bin:$PATH"

echo "[1] evil-winrm (ruby-dev bilan)..."
sudo apt-get install -y -qq ruby-dev libffi-dev >/dev/null 2>&1
sudo gem install evil-winrm 2>&1 | tail -2
command -v evil-winrm >/dev/null && echo "  ✓ evil-winrm" || echo "  ✗ evil-winrm"

echo "[2] enum4linux-ng (git + symlink)..."
if [ ! -d /opt/enum4linux-ng ]; then
  sudo git clone --depth 1 -q https://github.com/cddmp/enum4linux-ng /opt/enum4linux-ng 2>/dev/null
  python3 -m pip install --break-system-packages -q ldap3 impacket 2>/dev/null
  sudo tee /usr/local/bin/enum4linux-ng >/dev/null <<'EOF'
#!/bin/bash
exec python3 /opt/enum4linux-ng/enum4linux-ng.py "$@"
EOF
  sudo chmod +x /usr/local/bin/enum4linux-ng
fi
command -v enum4linux-ng >/dev/null && echo "  ✓ enum4linux-ng" || echo "  ✗ enum4linux-ng"

echo "[3] netexec (nxc) — pipx force / xato ko'rish..."
pipx install netexec --force 2>&1 | tail -3
command -v nxc >/dev/null && echo "  ✓ netexec (nxc)" || echo "  ✗ netexec (impacket+smbmap yetarli)"

echo
echo "==== YAKUNIY ATTACK PACK ===="
for t in nuclei feroxbuster evil-winrm wpscan nxc smbmap enum4linux-ng searchsploit; do
  command -v "$t" >/dev/null 2>&1 && printf "  ✓ %s\n" "$t" || printf "  ✗ %s\n" "$t"
done
