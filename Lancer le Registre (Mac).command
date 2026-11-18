#!/bin/bash
# Le Registre du Seigneur - lanceur macOS : double-cliquez sur ce fichier.
cd "$(dirname "$0")" || exit 1

# Python 3.7 or newer, even when it is not in the PATH of this window
# (python.org installer, Homebrew on Apple silicon or Intel, MacPorts, Anaconda/Miniconda, pyenv).
ok() { "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)' >/dev/null 2>&1; }
PY=""
candidates=()
for d in /Library/Frameworks/Python.framework/Versions/3.*/bin/python3; do candidates+=("$d"); done
candidates+=(/opt/homebrew/bin/python3 /usr/local/bin/python3 /opt/local/bin/python3)
p="$(command -v python3 2>/dev/null)"; [ -n "$p" ] && candidates+=("$p")
for d in "$HOME"/anaconda3/bin/python3 "$HOME"/miniconda3/bin/python3 "$HOME"/opt/anaconda3/bin/python3 \
         /opt/anaconda3/bin/python3 /opt/miniconda3/bin/python3 "$HOME"/.pyenv/shims/python3; do candidates+=("$d"); done
# Apple's /usr/bin/python3 only works once the "command line tools" are installed; otherwise it opens an install window
if [ "$(uname)" != "Darwin" ] || xcode-select -p >/dev/null 2>&1; then candidates+=(/usr/bin/python3); fi
for c in "${candidates[@]}"; do
  [ -x "$c" ] || continue
  [ "$c" = /usr/bin/python3 ] && [ "$(uname)" = "Darwin" ] && ! xcode-select -p >/dev/null 2>&1 && continue
  if ok "$c"; then PY="$c"; break; fi
done

if [ -n "$PY" ]; then
  echo "Démarrage du Registre du Seigneur… (gardez cette fenêtre ouverte pendant l'utilisation)"
  exec "$PY" start.py
fi
echo "Python 3 est introuvable sur ce Mac."
echo "- Installez-le depuis https://www.python.org/downloads/ (le plus simple), puis relancez ce fichier."
echo "- Sans Python : ouvrez simplement registre-du-seigneur.html (avec Chrome ou Edge, l'enregistrement est automatique)."
open "https://www.python.org/downloads/" 2>/dev/null
read -r -p "Appuyez sur Entrée pour fermer cette fenêtre."
