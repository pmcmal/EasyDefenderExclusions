"""
Easy Defender Exclusions
------------------------
Narzędzie GUI do zarządzania wyjątkami (wykluczeniami) Microsoft Defender oraz
globalnym włączaniem/wyłączaniem ochrony. PL/EN.

GUI tool to manage Microsoft Defender exclusions (folders, files, processes,
extensions) and toggle overall protection. PL/EN.

Używa wyłącznie oficjalnych cmdletów PowerShell (Get/Add/Remove/Set-MpPreference),
działa na własnej maszynie i wymaga uprawnień administratora.
"""

import ctypes
import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_NAME = "Easy Defender Exclusions"
APP_VERSION = "2.0.0"
CREATE_NO_WINDOW = 0x08000000

EXCLUSION_KEYS = ("path", "process", "extension")
EXCLUSION_PROPERTY = {
    "path": "ExclusionPath",
    "process": "ExclusionProcess",
    "extension": "ExclusionExtension",
}

# --------------------------------------------------------------------------- #
#  i18n
# --------------------------------------------------------------------------- #
LANG = "pl"

TR = {
    "pl": {
        "header_title": "Zarządzanie wyjątkami Microsoft Defender",
        "header_sub": "Dodawaj i usuwaj wykluczenia folderów, plików, programów i rozszerzeń. "
        "Wymaga uprawnień administratora.",
        "tab_path": "Foldery i pliki",
        "tab_process": "Procesy / programy",
        "tab_extension": "Rozszerzenia",
        "tab_protection": "Ochrona",
        "btn_folder": "Folder…",
        "btn_file": "Plik…",
        "btn_program": "Program…",
        "btn_add": "Dodaj wyjątek",
        "btn_remove": "Usuń zaznaczony",
        "btn_refresh": "Odśwież",
        "hint_path": "Pełna ścieżka do folderu lub pliku, np. D:\\Projekty\\build",
        "hint_process": "Nazwa programu (np. game.exe) lub pełna ścieżka do .exe",
        "hint_extension": "Rozszerzenie bez kropki, np. iso lub tmp",
        "items": "pozycji",
        "ready": "Gotowe.",
        "working": "Proszę czekać…",
        "added": "Dodano wyjątek: {v}",
        "removed": "Usunięto wyjątek: {v}",
        "confirm_remove": "Usunąć wyjątek?\n\n{v}",
        "err_add": "Nie udało się dodać wyjątku.\n\n{e}",
        "err_remove": "Nie udało się usunąć wyjątku.\n\n{e}",
        "dlg_folder": "Wybierz folder do wykluczenia",
        "dlg_file": "Wybierz plik do wykluczenia",
        "dlg_program": "Wybierz program (.exe) do wykluczenia",
        "ft_programs": "Programy",
        "ft_all": "Wszystkie pliki",
        "defender_warn": "Uwaga: nie udało się odczytać stanu Defendera (Get-MpPreference).",
        # Protection tab
        "prot_title": "Globalna ochrona Microsoft Defender",
        "prot_sub": "Włącza lub wyłącza wszystkie główne moduły ochrony naraz (skanowanie "
        "w czasie rzeczywistym, monitorowanie zachowań, PUA, chmura, próbki).",
        "tamper_title": "Ważne — Tamper Protection",
        "tamper_body": "Jeśli w Windows włączona jest „Ochrona przed naruszeniami” (Tamper "
        "Protection), wyłączanie ochrony przez te polecenia zostanie zignorowane przez "
        "system — to zabezpieczenie Windows, nie błąd aplikacji. Aby wyłączanie zadziałało, "
        "wyłącz Tamper Protection ręcznie w Zabezpieczeniach Windows.",
        "open_security": "Otwórz Zabezpieczenia Windows →",
        "prot_enable": "Włącz pełną ochronę",
        "prot_disable": "Wyłącz ochronę",
        "prot_refresh": "Odśwież stan",
        "prot_state": "Aktualny stan",
        "confirm_enable": "Czy na pewno włączyć pełną ochronę?",
        "confirm_disable": "Czy na pewno wyłączyć ochronę?",
        "tamper_warn": "Polecenia wysłano, ale Tamper Protection jest WŁĄCZONA — Windows mógł "
        "zignorować wyłączenie ochrony. Wyłącz Tamper Protection ręcznie i spróbuj ponownie.",
        "prot_changed": "Zmieniono ustawienia ochrony.",
        "prot_disabled_sent": "Wysłano żądanie wyłączenia ochrony.",
        "prot_err": "Część poleceń zwróciła błąd.\n\n{e}",
        "lbl_realtime": "Skanowanie w czasie rzeczywistym",
        "lbl_behavior": "Monitorowanie zachowań",
        "lbl_pua": "Ochrona PUA",
        "lbl_tamper": "Tamper Protection (naruszenia)",
        "on": "WŁĄCZONE",
        "off": "wyłączone",
        "pua_0": "Wyłączona",
        "pua_1": "Włączona",
        "pua_2": "Tryb audytu",
    },
    "en": {
        "header_title": "Microsoft Defender exclusions manager",
        "header_sub": "Add and remove exclusions for folders, files, programs and extensions. "
        "Requires administrator rights.",
        "tab_path": "Folders & files",
        "tab_process": "Processes / programs",
        "tab_extension": "Extensions",
        "tab_protection": "Protection",
        "btn_folder": "Folder…",
        "btn_file": "File…",
        "btn_program": "Program…",
        "btn_add": "Add exclusion",
        "btn_remove": "Remove selected",
        "btn_refresh": "Refresh",
        "hint_path": "Full path to a folder or file, e.g. D:\\Projects\\build",
        "hint_process": "Program name (e.g. game.exe) or full path to the .exe",
        "hint_extension": "Extension without the dot, e.g. iso or tmp",
        "items": "items",
        "ready": "Ready.",
        "working": "Please wait…",
        "added": "Added exclusion: {v}",
        "removed": "Removed exclusion: {v}",
        "confirm_remove": "Remove exclusion?\n\n{v}",
        "err_add": "Could not add the exclusion.\n\n{e}",
        "err_remove": "Could not remove the exclusion.\n\n{e}",
        "dlg_folder": "Select a folder to exclude",
        "dlg_file": "Select a file to exclude",
        "dlg_program": "Select a program (.exe) to exclude",
        "ft_programs": "Programs",
        "ft_all": "All files",
        "defender_warn": "Warning: could not read Defender status (Get-MpPreference).",
        "prot_title": "Microsoft Defender overall protection",
        "prot_sub": "Turns all main protection modules on or off at once (real-time scanning, "
        "behavior monitoring, PUA, cloud, sample submission).",
        "tamper_title": "Important — Tamper Protection",
        "tamper_body": "If Windows Tamper Protection is enabled, turning protection off via these "
        "commands will be ignored by the system — that is a Windows safeguard, not an app bug. "
        "For disabling to work, turn Tamper Protection off manually in Windows Security.",
        "open_security": "Open Windows Security →",
        "prot_enable": "Enable full protection",
        "prot_disable": "Disable protection",
        "prot_refresh": "Refresh state",
        "prot_state": "Current state",
        "confirm_enable": "Enable full protection?",
        "confirm_disable": "Disable protection?",
        "tamper_warn": "Commands were sent, but Tamper Protection is ON — Windows may have ignored "
        "disabling protection. Turn Tamper Protection off manually and try again.",
        "prot_changed": "Protection settings changed.",
        "prot_disabled_sent": "Disable-protection request sent.",
        "prot_err": "Some commands returned an error.\n\n{e}",
        "lbl_realtime": "Real-time scanning",
        "lbl_behavior": "Behavior monitoring",
        "lbl_pua": "PUA protection",
        "lbl_tamper": "Tamper Protection",
        "on": "ON",
        "off": "off",
        "pua_0": "Disabled",
        "pua_1": "Enabled",
        "pua_2": "Audit mode",
    },
}


def t(key: str, **kwargs) -> str:
    text = TR[LANG].get(key, key)
    return text.format(**kwargs) if kwargs else text


def resource_path(rel: str) -> str:
    """Ścieżka do zasobu, działa też w .exe z PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


# --------------------------------------------------------------------------- #
#  Uprawnienia administratora
# --------------------------------------------------------------------------- #
def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def relaunch_as_admin() -> None:
    executable = sys.executable
    params = "" if getattr(sys, "frozen", False) else f'"{os.path.abspath(__file__)}"'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)


# --------------------------------------------------------------------------- #
#  Warstwa PowerShell / Defender
# --------------------------------------------------------------------------- #
def run_powershell(command: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive",
             "-ExecutionPolicy", "Bypass", "-Command", command],
            capture_output=True, text=True,
            creationflags=CREATE_NO_WINDOW, timeout=60,
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, (result.stderr.strip() or result.stdout.strip() or "Unknown error.")
    except FileNotFoundError:
        return False, "PowerShell not found."
    except subprocess.TimeoutExpired:
        return False, "PowerShell timed out."
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def get_exclusions(property_name: str) -> list[str]:
    cmd = f"$v = (Get-MpPreference).{property_name}; if ($v) {{ $v -join \"`n\" }}"
    ok, out = run_powershell(cmd)
    if not ok or not out:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def add_exclusion(property_name: str, value: str) -> tuple[bool, str]:
    safe = value.replace("'", "''")
    return run_powershell(f"Add-MpPreference -{property_name} '{safe}' -ErrorAction Stop")


def remove_exclusion(property_name: str, value: str) -> tuple[bool, str]:
    safe = value.replace("'", "''")
    return run_powershell(f"Remove-MpPreference -{property_name} '{safe}' -ErrorAction Stop")


def defender_available() -> bool:
    ok, _ = run_powershell("Get-MpComputerStatus -ErrorAction Stop | Out-Null")
    return ok


def get_protection_status() -> dict:
    cmd = (
        "$s = Get-MpComputerStatus; $p = Get-MpPreference; "
        "'RealTime=' + $s.RealTimeProtectionEnabled; "
        "'Tamper=' + $s.IsTamperProtected; "
        "'Behavior=' + $s.BehaviorMonitorEnabled; "
        "'PUA=' + $p.PUAProtection"
    )
    ok, out = run_powershell(cmd)
    status: dict = {}
    if ok:
        for line in out.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                status[k.strip()] = v.strip()
    return status


PROTECTION_OFF = [
    "Set-MpPreference -DisableRealtimeMonitoring $true",
    "Set-MpPreference -DisableBehaviorMonitoring $true",
    "Set-MpPreference -DisableIOAVProtection $true",
    "Set-MpPreference -PUAProtection Disabled",
    "Set-MpPreference -MAPSReporting 0",
    "Set-MpPreference -SubmitSamplesConsent 2",
]
PROTECTION_ON = [
    "Set-MpPreference -DisableRealtimeMonitoring $false",
    "Set-MpPreference -DisableBehaviorMonitoring $false",
    "Set-MpPreference -DisableIOAVProtection $false",
    "Set-MpPreference -PUAProtection Enabled",
    "Set-MpPreference -MAPSReporting 2",
    "Set-MpPreference -SubmitSamplesConsent 1",
]


def set_protection(enable: bool) -> tuple[bool, str]:
    commands = PROTECTION_ON if enable else PROTECTION_OFF
    joined = "; ".join(f"try {{ {c} -ErrorAction Stop }} catch {{ Write-Error $_ }}" for c in commands)
    return run_powershell(joined)


# --------------------------------------------------------------------------- #
#  GUI
# --------------------------------------------------------------------------- #
class ExclusionTab(ttk.Frame):
    def __init__(self, master, type_key: str, app: "App"):
        super().__init__(master, padding=12)
        self.type_key = type_key
        self.property_name = EXCLUSION_PROPERTY[type_key]
        self.app = app
        self._build()
        self.refresh()

    def _build(self) -> None:
        add_bar = ttk.Frame(self)
        add_bar.pack(fill="x", pady=(0, 10))

        self.entry = ttk.Entry(add_bar)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.entry.bind("<Return>", lambda _e: self.on_add())

        if self.type_key == "path":
            ttk.Button(add_bar, text=t("btn_folder"), command=self.pick_folder).pack(side="left", padx=2)
            ttk.Button(add_bar, text=t("btn_file"), command=self.pick_file).pack(side="left", padx=2)
        elif self.type_key == "process":
            ttk.Button(add_bar, text=t("btn_program"), command=self.pick_process).pack(side="left", padx=2)

        ttk.Button(add_bar, text=t("btn_add"), command=self.on_add).pack(side="left", padx=2)

        ttk.Label(self, text=t(f"hint_{self.type_key}"), foreground="#666").pack(anchor="w", pady=(0, 6))

        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True)
        self.listbox = tk.Listbox(list_frame, activestyle="none", height=10)
        self.listbox.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scroll.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scroll.set)
        self.listbox.bind("<Delete>", lambda _e: self.on_remove())

        bottom = ttk.Frame(self)
        bottom.pack(fill="x", pady=(10, 0))
        ttk.Button(bottom, text=t("btn_remove"), command=self.on_remove).pack(side="left")
        ttk.Button(bottom, text=t("btn_refresh"), command=self.refresh).pack(side="left", padx=6)
        self.count_label = ttk.Label(bottom, text="")
        self.count_label.pack(side="right")

    def pick_folder(self) -> None:
        path = filedialog.askdirectory(title=t("dlg_folder"))
        if path:
            self.entry.delete(0, "end")
            self.entry.insert(0, os.path.normpath(path))

    def pick_file(self) -> None:
        path = filedialog.askopenfilename(title=t("dlg_file"))
        if path:
            self.entry.delete(0, "end")
            self.entry.insert(0, os.path.normpath(path))

    def pick_process(self) -> None:
        path = filedialog.askopenfilename(
            title=t("dlg_program"),
            filetypes=[(t("ft_programs"), "*.exe"), (t("ft_all"), "*.*")],
        )
        if path:
            self.entry.delete(0, "end")
            self.entry.insert(0, os.path.normpath(path))

    def on_add(self) -> None:
        value = self.entry.get().strip().strip('"')
        if not value:
            return

        def done(res, exc):
            ok, err = res if res else (False, str(exc))
            if ok:
                self.entry.delete(0, "end")
                self.refresh()
                self.app.set_status(t("added", v=value))
            else:
                messagebox.showerror(APP_NAME, t("err_add", e=err))

        self.app.run_bg(lambda: add_exclusion(self.property_name, value), done, t("working"))

    def on_remove(self) -> None:
        sel = self.listbox.curselection()
        if not sel:
            return
        value = self.listbox.get(sel[0])
        if not messagebox.askyesno(APP_NAME, t("confirm_remove", v=value)):
            return

        def done(res, exc):
            ok, err = res if res else (False, str(exc))
            if ok:
                self.refresh()
                self.app.set_status(t("removed", v=value))
            else:
                messagebox.showerror(APP_NAME, t("err_remove", e=err))

        self.app.run_bg(lambda: remove_exclusion(self.property_name, value), done, t("working"))

    def refresh(self) -> None:
        self.app.run_bg(
            lambda: get_exclusions(self.property_name),
            lambda res, exc: self._fill(res or []),
        )

    def _fill(self, items) -> None:
        self.listbox.delete(0, "end")
        for item in items:
            self.listbox.insert("end", item)
        self.count_label.config(text=f"{len(items)} {t('items')}")


class ProtectionTab(ttk.Frame):
    def __init__(self, master, app: "App"):
        super().__init__(master, padding=12)
        self.app = app
        self._build()
        self.refresh()

    def _build(self) -> None:
        ttk.Label(self, text=t("prot_title"), font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ttk.Label(self, text=t("prot_sub"), foreground="#555", wraplength=600).pack(anchor="w", pady=(0, 10))

        warn = ttk.LabelFrame(self, text=t("tamper_title"), padding=10)
        warn.pack(fill="x", pady=(0, 12))
        ttk.Label(warn, text=t("tamper_body"), foreground="#8a5a00", wraplength=600, justify="left").pack(anchor="w")
        ttk.Button(warn, text=t("open_security"), command=self.open_security).pack(anchor="w", pady=(8, 0))

        btns = ttk.Frame(self)
        btns.pack(fill="x", pady=(0, 10))
        ttk.Button(btns, text=t("prot_enable"), command=lambda: self.toggle(True)).pack(side="left", padx=(0, 8))
        ttk.Button(btns, text=t("prot_disable"), command=lambda: self.toggle(False)).pack(side="left")
        ttk.Button(btns, text=t("prot_refresh"), command=self.refresh).pack(side="right")

        box = ttk.LabelFrame(self, text=t("prot_state"), padding=10)
        box.pack(fill="both", expand=True)
        self.status_text = tk.StringVar(value="…")
        ttk.Label(box, textvariable=self.status_text, justify="left", font=("Consolas", 10)).pack(anchor="w")

    def open_security(self) -> None:
        subprocess.Popen(["cmd", "/c", "start", "", "windowsdefender://threatsettings"], shell=False)

    def toggle(self, enable: bool) -> None:
        if not messagebox.askyesno(APP_NAME, t("confirm_enable") if enable else t("confirm_disable")):
            return

        def work():
            ok, err = set_protection(enable)
            return ok, err, get_protection_status()

        def done(res, exc):
            if not res:
                messagebox.showerror(APP_NAME, t("prot_err", e=str(exc)))
                return
            ok, err, status = res
            self._render_status(status)
            tamper = status.get("Tamper", "").lower()
            if not enable and tamper == "true":
                messagebox.showwarning(APP_NAME, t("tamper_warn"))
            elif ok:
                self.app.set_status(t("prot_changed") if enable else t("prot_disabled_sent"))
            else:
                messagebox.showerror(APP_NAME, t("prot_err", e=err))

        self.app.run_bg(work, done, t("working"))

    def refresh(self) -> None:
        self.app.run_bg(get_protection_status, lambda res, exc: self._render_status(res or {}))

    def _render_status(self, s: dict) -> None:
        def yn(v: str) -> str:
            return {"true": t("on"), "false": t("off")}.get(v.lower(), v or "?")

        pua = s.get("PUA", "")
        pua_label = t(f"pua_{pua}") if pua in ("0", "1", "2") else (pua or "?")
        lines = [
            f"{t('lbl_realtime'):<34}: {yn(s.get('RealTime', '?'))}",
            f"{t('lbl_behavior'):<34}: {yn(s.get('Behavior', '?'))}",
            f"{t('lbl_pua'):<34}: {pua_label}",
            f"{t('lbl_tamper'):<34}: {yn(s.get('Tamper', '?'))}",
        ]
        self.status_text.set("\n".join(lines))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME}  v{APP_VERSION}")
        self.geometry("700x560")
        self.minsize(580, 440)
        self._busy_count = 0
        self.status = None
        self._bg_queue: queue.Queue = queue.Queue()
        self._set_icon()
        self._build_ui()
        self._poll_queue()
        if not defender_available():
            self.set_status(t("defender_warn"))

    def _set_icon(self) -> None:
        try:
            self.iconbitmap(resource_path(os.path.join("assets", "padlock.ico")))
        except Exception:
            try:
                self._icon_img = tk.PhotoImage(file=resource_path(os.path.join("assets", "padlock.png")))
                self.iconphoto(True, self._icon_img)
            except Exception:
                pass

    def _build_ui(self) -> None:
        self.header = ttk.Frame(self, padding=(10, 10, 10, 4))
        self.header.pack(fill="x")

        top = ttk.Frame(self.header)
        top.pack(fill="x")
        self.title_lbl = ttk.Label(top, text=t("header_title"), font=("Segoe UI", 13, "bold"))
        self.title_lbl.pack(side="left", anchor="w")
        self._build_lang_switch(top)

        self.sub_lbl = ttk.Label(self.header, text=t("header_sub"), foreground="#555", wraplength=660)
        self.sub_lbl.pack(anchor="w", pady=(2, 0))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(6, 6))
        for key in EXCLUSION_KEYS:
            self.notebook.add(ExclusionTab(self.notebook, key, self), text=t(f"tab_{key}"))
        self.notebook.add(ProtectionTab(self.notebook, self), text=t("tab_protection"))

        self.status = ttk.Label(self, text=t("ready"), relief="sunken", anchor="w", padding=4)
        self.status.pack(fill="x", side="bottom")

    def _build_lang_switch(self, parent) -> None:
        box = ttk.Frame(parent)
        box.pack(side="right")
        self.lang_var = tk.StringVar(value=LANG)
        for code in ("pl", "en"):
            ttk.Radiobutton(
                box, text=code.upper(), value=code, variable=self.lang_var,
                command=self.change_language,
            ).pack(side="left")

    def change_language(self) -> None:
        global LANG
        new = self.lang_var.get()
        if new == LANG:
            return
        LANG = new
        self.header.destroy()
        self.notebook.destroy()
        self.status.destroy()
        self._build_ui()

    def set_status(self, text: str) -> None:
        if getattr(self, "status", None) is not None:
            self.status.config(text=text)

    # -- praca w tle (nie blokuje UI) ------------------------------------- #
    def run_bg(self, work, done=None, busy_msg=None) -> None:
        """Uruchamia blokujące `work()` w wątku, wynik oddaje do `done` w wątku UI."""
        self._set_busy(True, busy_msg)

        def worker():
            try:
                result, err = work(), None
            except Exception as exc:  # noqa: BLE001
                result, err = None, exc
            # Wynik przekazujemy do wątku UI przez kolejkę (after() nie jest thread-safe).
            self._bg_queue.put((result, err, done))

        threading.Thread(target=worker, daemon=True).start()

    def _poll_queue(self) -> None:
        """Działa w wątku UI: odbiera gotowe wyniki i uruchamia ich callbacki."""
        try:
            while True:
                result, err, done = self._bg_queue.get_nowait()
                self._set_busy(False)
                if done is not None:
                    done(result, err)
        except queue.Empty:
            pass
        try:
            self.after(60, self._poll_queue)
        except Exception:
            pass  # okno zamknięte

    def _set_busy(self, busy: bool, msg: str | None = None) -> None:
        self._busy_count = max(self._busy_count + (1 if busy else -1), 0)
        try:
            self.config(cursor="watch" if self._busy_count else "")
        except Exception:
            pass
        if busy and msg:
            self.set_status(msg)
        elif not busy and self._busy_count == 0:
            # wyczyść komunikat „proszę czekać", jeśli nikt nie ustawił innego
            if getattr(self, "status", None) is not None and self.status.cget("text") == t("working"):
                self.set_status(t("ready"))


def main() -> None:
    if os.name != "nt":
        print("This program runs on Windows only.")
        sys.exit(1)
    if not is_admin():
        relaunch_as_admin()
        sys.exit(0)
    App().mainloop()


if __name__ == "__main__":
    main()
