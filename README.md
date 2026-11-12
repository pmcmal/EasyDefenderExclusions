<div align="center">

# 🔒 Easy Defender Exclusions

**Aplikacja GUI do zarządzania wyjątkami Microsoft Defender — foldery, pliki, programy, rozszerzenia — oraz globalnym włączaniem/wyłączaniem ochrony.**

</div>

---

<details open>
<summary><b>🇵🇱 Polski</b></summary>

## Co to jest?

Prosta aplikacja z interfejsem graficznym (Python + Tkinter) do zarządzania ustawieniami
Microsoft Defender na **własnym komputerze**. Zastępuje stare skrypty `.bat` jednym
programem `.exe` z ikoną i przełącznikiem języka **PL/EN**.

Używa wyłącznie oficjalnych poleceń PowerShell Microsoftu
(`Get-/Add-/Remove-/Set-MpPreference`) — nic nie jest obchodzone „na siłę".

## Funkcje

- **Foldery i pliki** — dodawaj i usuwaj wykluczenia ścieżek (z oknem wyboru folderu/pliku).
- **Procesy / programy** — wykluczaj konkretny program (np. `game.exe` lub pełną ścieżkę do `.exe`).
- **Rozszerzenia** — wykluczaj typy plików (np. `iso`, `tmp`).
- **Ochrona** — włącz lub wyłącz wszystkie główne moduły ochrony naraz, z podglądem aktualnego stanu.
- **Przełącznik PL / EN** w prawym górnym rogu.
- Automatyczne pytanie o uprawnienia administratora (UAC) przy starcie.

## Pobieranie

Gotowy plik `EasyDefenderExclusions.exe` znajdziesz w zakładce
[**Releases**](../../releases). Nie wymaga instalacji — po prostu uruchom.

## ⚠️ Ważne — Tamper Protection

Windows 10/11 ma domyślnie włączoną **Ochronę przed naruszeniami (Tamper Protection)**.
Gdy jest aktywna, system **ignoruje** wyłączanie ochrony przez jakiekolwiek polecenia
(dlatego stare skrypty `.bat` przestały działać). Aby wyłączanie ochrony zadziałało,
trzeba Tamper Protection wyłączyć ręcznie w *Zabezpieczenia Windows → Ochrona przed
wirusami i zagrożeniami → Zarządzaj ustawieniami*. Przycisk w aplikacji otwiera ten panel.

**Wyjątki (wykluczenia) działają niezależnie od Tamper Protection** — to główna i zawsze
sprawna funkcja aplikacji.

## Budowanie ze źródeł

```bash
pip install -r requirements.txt
python make_icon.py     # generuje ikonę kłódki
python build.py         # tworzy dist/EasyDefenderExclusions.exe
```

## ⚠️ Ostrzeżenie

Używasz tego narzędzia na własną odpowiedzialność i na własnym komputerze. Wyłączenie
ochrony antywirusowej naraża system na realne zagrożenia — rób to świadomie i tylko
tymczasowo. Zawsze sprawdzaj źródła plików, które dodajesz do wyjątków.

## Technologia

- **Język:** Python 3 (Tkinter GUI)
- **Build:** PyInstaller (pojedynczy `.exe`, manifest administratora, ikona)
- **Wymagania:** Windows 10 lub 11

</details>

<details>
<summary><b>🇬🇧 English</b></summary>

## What is it?

A simple GUI application (Python + Tkinter) for managing Microsoft Defender settings on
**your own computer**. It replaces the old `.bat` scripts with a single `.exe` that has an
icon and a **PL/EN** language switch.

It uses only Microsoft's official PowerShell commands
(`Get-/Add-/Remove-/Set-MpPreference`) — nothing is forcibly bypassed.

## Features

- **Folders & files** — add and remove path exclusions (with a folder/file picker).
- **Processes / programs** — exclude a specific program (e.g. `game.exe` or a full `.exe` path).
- **Extensions** — exclude file types (e.g. `iso`, `tmp`).
- **Protection** — enable or disable all main protection modules at once, with a live status view.
- **PL / EN switch** in the top-right corner.
- Prompts for administrator rights (UAC) automatically on launch.

## Download

Grab the ready-made `EasyDefenderExclusions.exe` from the
[**Releases**](../../releases) tab. No installation required — just run it.

## ⚠️ Important — Tamper Protection

Windows 10/11 ships with **Tamper Protection** enabled by default. While it is on, the
system **ignores** any command that tries to turn protection off (which is why the old
`.bat` scripts stopped working). To disable protection, turn Tamper Protection off manually
in *Windows Security → Virus & threat protection → Manage settings*. The in-app button
opens that panel.

**Exclusions work regardless of Tamper Protection** — they are the app's core, always-working feature.

## Building from source

```bash
pip install -r requirements.txt
python make_icon.py     # generates the padlock icon
python build.py         # produces dist/EasyDefenderExclusions.exe
```

## ⚠️ Warning

You use this tool at your own risk, on your own machine. Disabling antivirus protection
exposes your system to real threats — do it deliberately and only temporarily. Always
verify the source of any files you add to the exclusion list.

## Tech

- **Language:** Python 3 (Tkinter GUI)
- **Build:** PyInstaller (single `.exe`, administrator manifest, icon)
- **Requirements:** Windows 10 or 11

</details>
