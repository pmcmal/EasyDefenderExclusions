"""Buduje pojedynczy plik EasyDefenderExclusions.exe (admin, ikona kłódki).
   Builds a single EasyDefenderExclusions.exe (admin manifest, padlock icon).

Użycie / usage:
    python make_icon.py          # najpierw wygeneruj ikonę / generate icon first
    python build.py              # zbuduj .exe / build the .exe

Wynik / output: dist/EasyDefenderExclusions.exe
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(HERE, "assets", "padlock.ico")


def main() -> None:
    if not os.path.exists(ICON):
        print("Brak ikony — uruchom najpierw: python make_icon.py")
        print("Icon missing — run first: python make_icon.py")
        sys.exit(1)

    args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--uac-admin",
        "--name", "EasyDefenderExclusions",
        "--icon", ICON,
        "--add-data", f"{ICON}{os.pathsep}assets",
        "--add-data", f"{os.path.join(HERE, 'assets', 'padlock.png')}{os.pathsep}assets",
        os.path.join(HERE, "easy_defender_exclusions.py"),
    ]
    print(" ".join(args))
    subprocess.run(args, check=True)
    print("\nGotowe / done -> dist/EasyDefenderExclusions.exe")


if __name__ == "__main__":
    main()
