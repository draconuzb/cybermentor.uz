#!/bin/bash
echo "==== AUTO-START HOLATI [enabled = reboot chidamli] ===="
for s in code-server@ubuntu nginx filebrowser panel fail2ban; do
  printf "  %-22s %s\n" "$s" "$(systemctl is-enabled "$s" 2>/dev/null)"
done
echo "==== SWAP ===="
grep -q swapfile /etc/fstab && echo "  swap: fstabda bor [doimiy]" || echo "  swap: fstabda yo'q"
echo "==== PATH ===="
grep -q '.local/bin' ~/.bashrc && echo "  ~/.local/bin PATHда bor [helperlar ishlaydi]"
echo "==== HOZIRGI HOLAT ===="
for s in code-server@ubuntu nginx filebrowser panel fail2ban; do
  printf "  %-22s %s\n" "$s" "$(systemctl is-active "$s" 2>/dev/null)"
done
