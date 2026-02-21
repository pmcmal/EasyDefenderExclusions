# DefenderControl-Scripts 🛡️

Zestaw prostych skryptów `.bat` (Windows Batch) do szybkiego zarządzania ustawieniami Windows Defender. Idealne dla osób, które często instalują oprogramowanie blokowane przez systemowe zabezpieczenia (np. fałszywe alarmy w grach/programach z torrentów).

## 🚀 Co znajdziesz w repozytorium?

1.  **`DEFENDER_OFF.bat`**: Całkowicie uśpiona ochrona. Wyłącza skanowanie w czasie rzeczywistym, ochronę w chmurze oraz wysyłanie próbek do Microsoftu.
2.  **`DEFENDER_ON.bat`**: Przywraca domyślne, bezpieczne ustawienia systemu jednym kliknięciem.
3.  **`ADD_EXCLUSION.bat`**: Pozwala dodać konkretny folder do "białej listy". Defender nigdy nie będzie zaglądał do plików w tej lokalizacji.

## 🛠️ Jak to działa? (Przykład)

Wyobraź sobie, że pobrałeś grę, a Windows natychmiast kasuje plik `steam_api.dll`.

1. Uruchom `ADD_EXCLUSION.bat`.
2. Podaj ścieżkę do folderu z grą (np. `D:\Gry\MojaGra`).
3. Gotowe! Teraz możesz wypakować pliki ponownie, a Defender je zignoruje.

> [!IMPORTANT]
> Skrypty wymagają uprawnień Administratora. Jeśli funkcja **Tamper Protection** (Ochrona przed naruszeniami) jest włączona w ustawieniach Windows, skrypty mogą zostać zablokowane. Należy ją wyłączyć ręcznie w panelu Zabezpieczenia Windows.

## 💻 Technologia
* **Język:** Windows Batch / PowerShell
* **Wymagania:** System Windows 10 lub 11

## ⚠️ Ostrzeżenie
Używasz tych skryptów na własną odpowiedzialność. Wyłączenie antywirusa naraża Twój komputer na realne zagrożenia. Zawsze sprawdzaj źródła plików, które instalujesz.
