@echo off
rem Lance le site sur le reseau local. Double-cliquer sur ce fichier.
rem Les autres postes ouvrent l'adresse affichee ci-dessous dans leur navigateur.
cd /d "%~dp0"
echo.
echo  Atelier des contes - serveur local
echo  Adresse pour les eleves (meme reseau) :
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do echo     http:%%a:8000/
echo  Sur ce poste : http://localhost:8000/
echo  Fermer cette fenetre pour arreter le serveur.
echo.
where py >nul 2>nul && (py -m http.server 8000 --bind 0.0.0.0 & goto :eof)
where python >nul 2>nul && (python -m http.server 8000 --bind 0.0.0.0 & goto :eof)
echo Python n'est pas installe : voir https://www.python.org/downloads/
pause
