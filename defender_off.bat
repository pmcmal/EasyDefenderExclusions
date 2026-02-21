@echo off
:: Sprawdzanie uprawnien administratora (tak samo jak w poprzednim)
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_commands
) else (
    echo Proba uzyskania uprawnien administratora...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_commands
echo [!] Wlaczanie wszystkich modulow Defender...

:: Włącza skanowanie w czasie rzeczywistym
powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $false"

:: Włącza blokowanie potencjalnie niechcianych aplikacji (PUA)
powershell -Command "Set-MpPreference -PUAProtection Enabled"

:: Włącza ochronę w chmurze (2 = Wysoki poziom raportowania)
powershell -Command "Set-MpPreference -MAPSReporting 2"

:: Włącza wysyłanie próbek (1 = Wysyłaj bezpieczne próbki automatycznie)
powershell -Command "Set-MpPreference -SubmitSamplesConsent 1"

:: Włącza monitorowanie zachowań (Behavior Monitoring)
powershell -Command "Set-MpPreference -DisableBehaviorMonitoring $false"

:: Włącza skanowanie plików pobranych z internetu
powershell -Command "Set-MpPreference -DisableIOAVProtection $false"

echo.
echo [+] Gotowe! Wszystkie systemy ochrony zostaly przywrocone.
pause