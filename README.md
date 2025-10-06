# CMUJ Wiki - Wiedza Medyczna

Wspólna baza wiedzy dla studentów medycyny na Collegium Medicum Uniwersytetu Jagiellońskiego.

🌐 **Live Site**: **[cmuj-wiki.github.io/wiki](https://cmuj-wiki.github.io/wiki)**

## 📚 O Projekcie

CMUJ Wiki to platforma stworzona przez studentów dla studentów, zawierająca:

- 📅 **Kalendarz zajęć** - harmonogramy dla wszystkich lat
- 📖 **Materiały do nauki** - notatki, skrypty, zasoby
- 🎯 **Kolokwia i egzaminy** - terminy, zakres materiału, porady
- ✅ **Testy** - zestawy pytań do ćwiczeń
- 👨‍⚕️ **Informacje o prowadzących**
- 🔗 **Przydatne linki** - MedBox, narzędzia, bibliografia

## 🚀 Dla Użytkowników

Po prostu odwiedź: **[cmuj-wiki.github.io/wiki](https://cmuj-wiki.github.io/wiki)**

## 🤝 Dla Współtwórców

Chcesz dodać materiały lub poprawić istniejące treści? Świetnie!

### Metoda 1: Edycja przez przeglądarkę (najłatwiejsza)

1. Znajdź stronę do edycji na wiki
2. Kliknij ikonę ✏️ (edit) w prawym górnym rogu
3. Wprowadź zmiany na GitHubie
4. Wyślij Pull Request

Szczegóły: [docs/jak-edytowac.md](docs/jak-edytowac.md)

### Metoda 2: Lokalna edycja (dla zaawansowanych)

1. **Sklonuj repozytorium**
   ```bash
   git clone https://github.com/cmuj-wiki/wiki.git
   cd wiki
   ```

2. **Zainstaluj zależności**
   ```bash
   pip install mkdocs-material
   ```

3. **Uruchom lokalny serwer**
   ```bash
   mkdocs serve
   ```
   Otwórz http://127.0.0.1:8000 w przeglądarce

4. **Edytuj pliki**
   - Wszystkie strony są w folderze `docs/`
   - Używaj Markdown (.md)
   - Zmiany widoczne od razu w przeglądarce

5. **Wyślij zmiany**
   ```bash
   git checkout -b moje-zmiany
   git add .
   git commit -m "Opis zmian"
   git push origin moje-zmiany
   ```
   Następnie utwórz Pull Request na GitHubie.

## 📁 Struktura Projektu

```
wiki/
├── docs/                      # Wszystkie strony wiki
│   ├── index.md              # Strona główna
│   ├── semestr-1/            # Rok I
│   ├── semestr-2/            # Rok I (sem. 2)
│   ├── kolokwia/             # Terminy i materiały do kolokwiów
│   ├── testy/                # Zestawy testów
│   ├── egzaminy/             # Egzaminy i LEK
│   ├── zasoby/               # Książki, linki, narzędzia
│   ├── prowadzacy/           # Informacje o prowadzących
│   ├── javascripts/          # Interaktywne komponenty
│   └── stylesheets/          # Stylowanie
│
├── data/                     # Strukturalne dane (kalendarze, etc.)
├── scripts/                  # Skrypty pomocnicze
├── mkdocs.yml                # Konfiguracja MkDocs
└── README.md                 # Ten plik
```

## 🛠️ Technologie

- **MkDocs Material** - generator stron statycznych
- **GitHub Pages** - hosting (całkowicie darmowy!)
- **Markdown** - format treści
- **Python** - skrypty pomocnicze

## 📝 Jak Dodać Nową Stronę?

1. Stwórz plik `.md` w odpowiednim folderze `docs/`
2. Dodaj link w `mkdocs.yml` w sekcji `nav:`
3. Wyślij Pull Request

Przykład:
```yaml
nav:
  - Semestr I:
    - Nowy przedmiot: semestr-1/nowy-przedmiot.md
```

## 🎨 Podstawy Markdown

```markdown
# Nagłówek 1
## Nagłówek 2

**Pogrubienie**
*Kursywa*

- Lista
- Punktowana

1. Lista
2. Numerowana

[Link](https://example.com)

!!! tip "Wskazówka"
    Treść wskazówki
```

Więcej w [dokumentacji MkDocs Material](https://squidfunk.github.io/mkdocs-material/reference/).

## 📋 Zasady Współpracy

- ✅ Dodawaj tylko materiały własne lub za zgodą autora
- ✅ Rzeczowe komentarze o prowadzących
- ✅ Sprawdź, czy materiał już nie istnieje
- ❌ Bez materiałów chronionych prawami autorskimi (bez zgody)
- ❌ Bez obraźliwych treści

## 📞 Kontakt

- 🐛 **Błędy**: [GitHub Issues](https://github.com/cmuj-wiki/wiki/issues)
- 💬 **Dyskusje**: [GitHub Discussions](https://github.com/cmuj-wiki/wiki/discussions)

## 📜 Licencja

Ten projekt jest open source. Treści wiki są tworzone przez społeczność studentów UJ CM.

Treści edukacyjne udostępniane są na zasadzie fair use dla celów edukacyjnych.

## 🙏 Podziękowania

Dziękujemy wszystkim studentom, którzy przyczynili się do rozwoju tego projektu!

---

**Stworzone przez studentów, dla studentów** 🩺

*Projekt studencki nieafiliowany oficjalnie z UJ Collegium Medicum*
