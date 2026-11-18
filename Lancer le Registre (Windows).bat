@echo off
rem Le Registre du Seigneur - lanceur Windows : double-cliquez sur ce fichier.
chcp 65001 >nul
cd /d "%~dp0"
set "PY="
rem 1. the usual commands (py launcher, python, python3); the Microsoft Store shortcut that only opens the Store is skipped
call :try py -3
call :try python
call :try python3
rem 2. Python installed but not in the PATH: look in the usual install folders
call :tryexe "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe"
call :tryexe "%SystemRoot%\py.exe"
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do call :tryexe "%%~D\python.exe"
for /d %%D in ("%ProgramFiles%\Python3*") do call :tryexe "%%~D\python.exe"
for /d %%D in ("%ProgramFiles(x86)%\Python3*") do call :tryexe "%%~D\python.exe"
for /d %%D in ("%SystemDrive%\Python3*") do call :tryexe "%%~D\python.exe"
for %%D in ("%USERPROFILE%\anaconda3" "%USERPROFILE%\miniconda3" "%LOCALAPPDATA%\anaconda3" "%LOCALAPPDATA%\miniconda3" "%ProgramData%\anaconda3" "%ProgramData%\miniconda3") do call :tryexe "%%~D\python.exe"
for /d %%D in ("%LOCALAPPDATA%\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3*") do call :tryexe "%%~D\python.exe"
if not defined PY goto nopy
echo Demarrage du Registre du Seigneur... (gardez cette fenetre ouverte pendant l'utilisation)
%PY% start.py
if errorlevel 1 pause
exit /b

:try
rem %* = a command; kept only if it really runs Python 3.7 or newer
if defined PY goto :eof
%* -c "import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)" >nul 2>nul
if errorlevel 1 goto :eof
set "PY=%*"
goto :eof

:tryexe
rem %1 = full path of a python.exe or py.exe
if defined PY goto :eof
if not exist "%~1" goto :eof
"%~1" -c "import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)" >nul 2>nul
if errorlevel 1 goto :eof
set PY="%~1"
goto :eof

:nopy
echo Python 3 est introuvable sur cet ordinateur.
echo - S'il n'est pas installe : installez-le depuis https://www.python.org/downloads/
echo   (cochez "Add python.exe to PATH" pendant l'installation), puis relancez ce fichier.
echo - S'il est installe ailleurs : ouvrez une invite de commandes dans ce dossier et tapez
echo   "C:\chemin\vers\python.exe" start.py
echo - Sans Python : ouvrez simplement registre-du-seigneur.html (enregistrement dans un fichier).
start "" https://www.python.org/downloads/
pause
