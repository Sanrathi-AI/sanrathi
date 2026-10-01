#!/usr/bin/env bash
# Linux version of guide sections 2.3, 2.4 and the firewall note.
# Windows used `setx OLLAMA_HOST 0.0.0.0` / `setx OLLAMA_CONTEXT_LENGTH 8192` and
# "allow Private networks only". On Linux Ollama is a systemd service, so we:
#   1. add a systemd override with the same two variables,
#   2. let only Docker's private networks (172.16.0.0/12) reach port 11434,
#      and block it for everyone else (cafe / hostel Wi-Fi).
# Run:  sudo bash sanrathi/linux/setup_ollama_host.sh
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Run with sudo"; exit 1; }

mkdir -p /etc/systemd/system/ollama.service.d
cat > /etc/systemd/system/ollama.service.d/sanrathi.conf <<'CONF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
CONF
systemctl daemon-reload
systemctl restart ollama
echo "Ollama override written and service restarted."

if command -v ufw >/dev/null; then
    ufw allow from 172.16.0.0/12 to any port 11434 proto tcp comment 'Ollama for Docker (Sanrathi)'
    ufw deny 11434/tcp comment 'Ollama blocked for LAN (Sanrathi)'
    if ufw status | grep -q "Status: active"; then
        echo "ufw is active: Docker can reach Ollama, other machines cannot."
    else
        echo "WARNING: ufw is INACTIVE, so port 11434 is open to your whole network."
        echo "         Rules are saved; turn the firewall on with:  sudo ufw enable"
    fi
else
    echo "WARNING: ufw not installed; port 11434 is reachable from your network."
    echo "         Install it (sudo apt install ufw) and rerun this script."
fi
sleep 2
curl -s http://127.0.0.1:11434/api/version && echo
