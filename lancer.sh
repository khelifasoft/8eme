#!/bin/sh
# Lance le site sur le réseau local : ./lancer.sh
cd "$(dirname "$0")" || exit 1
echo
echo " Atelier des contes - serveur local"
echo " Adresse pour les élèves (même réseau) :"
for ip in $(hostname -I 2>/dev/null); do echo "    http://$ip:8000/"; done
echo " Sur ce poste : http://localhost:8000/"
echo " Ctrl+C pour arrêter."
echo
exec python3 -m http.server 8000 --bind 0.0.0.0
