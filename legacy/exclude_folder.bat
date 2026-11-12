@echo off
:: Sprawdzanie uprawnień administratora
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_commands
) else (
    echo [!] Proba uzyskania uprawnien administratora...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_commands
echo ======================================================
echo    DODAWANIE FOLDERU DO WYJATKOW WINDOWS DEFENDER
echo ======================================================
echo.
echo Wpisz lub wklej sciezke folderu (np. C:\Gry\MojaGra):
set /p folderPath="Sciezka: "

:: Usuwanie cudzysłowów, jeśli użytkownik wkleił ścieżkę w cudzysłowie
set folderPath=%folderPath:"=%

if "%folderPath%"=="" (
    echo [Blad] Nie podano sciezki!
    pause
    exit /b
)

echo.
echo [!] Dodaje folder: "%folderPath%" do wyjatkow...

:: Wywołanie komendy PowerShell dodającej folder
powershell -Command "Add-MpPreference -ExclusionPath '%folderPath%'"

if %errorLevel% == 0 (
    echo [+] Sukces! Defender bedzie ignorowal ten folder.
) else (
    echo [-] Wystapil blad. Sprawdz czy sciezka jest poprawna.
)

echo.
pause