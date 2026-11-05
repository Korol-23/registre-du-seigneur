#!/bin/bash
# Le Registre du Seigneur - lanceur macOS : double-cliquez sur ce fichier.
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then
  echo "Démarrage du Registre du Seigneur… (gardez cette fenêtre ouverte pendant l'utilisation)"
  exec python3 start.py
fi
echo "Python 3 n'est pas installé sur ce Mac."
echo "Installez-le depuis https://www.python.org/downloads/ puis relancez ce fichier."
open "https://www.python.org/downloads/"
read -r -p "Appuyez sur Entrée pour fermer cette fenêtre."
