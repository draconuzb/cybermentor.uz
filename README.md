# cybermentor.uz — CTF Control Platform

Brauzer orqali ishlaydigan CTF boshqaruv platformasi va CyberKent CTF uchun tayyorlangan attack-box konfiguratsiyasi. AWS EC2 (Ubuntu) ustida qurilgan: code-server (VS Code in browser) + nginx + Cloudflare, custom Flask boshqaruv paneli, va CTF ish quroli to'plami.

> **Eslatma:** Bu repo shaxsiy (private). Jonli maxfiy fayllar (VPN kaliti, SSH kalitlar, parollar, `filebrowser.db`, sertifikatlar) ataylab kiritilmagan — ular faqat serverda turadi.

## Tuzilishi

| Papka / fayl | Tavsif |
|---|---|
| `ctf_*.sh` | Serverni sozlash skriptlari (tool o'rnatish, hardening, VPN, kategoriyalar) |
| `dash_setup.sh`, `panel/`, `panel_app.py` | "CyberKent Red Team" Flask boshqaruv paneli |
| `attack_pack.sh`, `attack_fix.sh`, `fb_fix.sh` | Attack tool va filebrowser o'rnatish |
| `helpers/` | Custom terminal buyruqlari: `recon`, `revshell`, `listen`, `serve`, `flag`, `ctf`, `vpn-*` |
| `config/nginx/` | nginx reverse-proxy konfigi |
| `config/systemd/` | `panel` va `filebrowser` systemd unitlari |
| `ctf/` | CTF workspace (web/crypto/forensics/rev/pwn/stego/misc) |
| `*.py`, `*.sh` (ildizda) | CyberKent CTF challenge yechim skriptlari (writeup materiali) |

## Server (qisqacha)

- **Stack:** code-server `127.0.0.1:8080` → nginx `:80/:443` → Cloudflare
- **Panel:** Flask + gunicorn `127.0.0.1:8090`, `/dash/` yo'nalishi
- **Filebrowser:** `127.0.0.1:8081`, `/files/` yo'nalishi
- **Tools:** nmap, ffuf, nuclei, sqlmap, impacket, evil-winrm, pwntools, volatility3 va h.k.

Parollar va kalitlar serverdagi tegishli fayllarda saqlanadi, bu repoda emas.
