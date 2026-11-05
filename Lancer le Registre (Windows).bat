@echo off
rem Le Registre du Seigneur - lanceur Windows : double-cliquez sur ce fichier.
chcp 65001 >nul
cd /d "%~dp0"
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY goto nopy
echo Demarrage du Registre du Seigneur... (gardez cette fenetre ouverte pendant l'utilisation)
%PY% start.py
if errorlevel 1 pause
exit /b
:nopy
echo Python 3 n'est pas installe sur cet ordinateur.
echo Installez-le depuis https://www.python.org/downloads/
echo (cochez "Add python.exe to PATH" pendant l'installation), puis relancez ce fichier.
start "" https://www.python.org/downloads/
pause
