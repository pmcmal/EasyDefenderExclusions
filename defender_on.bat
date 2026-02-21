@echo off
:: Sprawdzanie uprawnien administratora
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_commands
) else (
    echo Proba uzyskania uprawnien administratora...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_commands
echo [!] Wylaczanie modulow Defender (Wersja Poprawiona)...

:: Wyłącza skanowanie w czasie rzeczywistym
powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"

:: Wyłącza blokowanie potencjalnie niechcianych aplikacji (np. instalatorów gier)
powershell -Command "Set-MpPreference -PUAProtection Disabled"

:: Wyłącza ochronę dostarczaną z chmury (zastępuje DisableCloudLookup)
:: 0 = Wyłączone
powershell -Command "Set-MpPreference -MAPSReporting 0"

:: Wyłącza wysyłanie próbek (2 = Nigdy nie wysyłaj)
powershell -Command "Set-MpPreference -SubmitSamplesConsent 2"

echo.
echo [+] Gotowe! Jesli nie widzisz bledow na czerwono, ochrona spi.
pause