# Jak dodać materiały do wiki?

## ⚠️ Wymagane hasło edytora

!!! warning "Dostęp do edycji wymaga specjalnego hasła"
    **WAŻNE:** Aby edytować strony wiki, potrzebujesz **hasła edytora** (nie zwykłego hasła studenckiego).

    - 🔒 **Hasło studenckie** - pozwala tylko przeglądać wiki (przycisk edycji ✏️ jest ukryty)
    - 🔓 **Hasło edytora** - pokazuje przycisk edycji ✏️ i pozwala wprowadzać zmiany

    **Jak uzyskać hasło edytora?**

    - Zapytaj starszego studenta lub administratora wiki na czacie grupy
    - Hasło edytora jest udostępniane tylko osobom, które chcą aktywnie współtworzyć wiki

!!! tip "Nie martw się - nie możesz nic zepsuć!"
    - Twoje zmiany są sprawdzane przed publikacją
    - GitHub zapisuje wszystko - każdą zmianę można cofnąć
    - Możesz eksperymentować bez obaw!

## 🎯 Dlaczego warto dodawać materiały?

- Pomagasz setkom studentów, którzy będą po Tobie
- Tworzysz bazę wiedzy, z której sam korzystasz
- To zabiera tylko kilka minut!

!!! success "Im więcej osób się zaangażuje, tym lepsze to narzędzie dla wszystkich!"

## 🚀 Metoda 1: Edycja przez przeglądarkę (NAJŁATWIEJSZA)

**Nie potrzebujesz żadnych programów** - wszystko robisz w przeglądarce!

### Krok 1: Znajdź stronę do edycji
1. Otwórz stronę przedmiotu, którą chcesz edytować
2. Kliknij ikonę ołówka (✏️) w prawym górnym rogu
3. Zostaniesz przekierowany na GitHub

### Krok 2: Zaloguj się (jeśli jeszcze nie masz konta)
1. Stwórz darmowe konto na [GitHub.com](https://github.com/signup)
2. To zabiera 2 minuty i jest **całkowicie za darmo**

### Krok 3: Edytuj plik

**Co zobaczysz:** GitHub pokaże Ci plik źródłowy w formacie **Markdown** (końcówka `.md`)

!!! info "Co to jest Markdown?"
    Markdown to prosty sposób formatowania tekstu - piszesz zwykły tekst ze specjalnymi znakami:

    - `**pogrubienie**` → **pogrubienie**
    - `*kursywa*` → *kursywa*
    - `# Nagłówek` → duży nagłówek

    To **NIE jest HTML** - to znacznie prostszy język! Edytujesz plik źródłowy (jak kod), a nie gotową stronę.

    💡 **Analogia:** To jak "zaproponuj zmiany" w Google Docs - edytujesz treść, a system sam ją sformatuje.

**Jak edytować:**

1. Kliknij ikonę ołówka (✏️), aby rozpocząć edycję
2. Wprowadź swoje zmiany w edytorze tekstowym
3. Zobacz [składnię Markdown](#skladnia-markdown) poniżej - to bardzo proste!
4. Przewiń na dół i kliknij "Propose changes" (zaproponuj zmiany)

### Krok 4: Wyślij propozycję (Pull Request)
1. GitHub stworzy "pull request" - propozycję zmiany
2. Opisz krótko, co zmieniłeś (np. "Dodano wykłady z anatomii 2024/2025")
3. Kliknij "Create pull request"
4. Gotowe! Twoja zmiana zostanie sprawdzona i dodana do wiki

!!! tip "Nie martw się o błędy"
    Zanim Twoje zmiany trafią na stronę, zostaną sprawdzone przez innych. Możesz eksperymentować bez obaw!

## 💻 Metoda 2: Edycja lokalna (dla zaawansowanych)

Jeśli znasz Git i chcesz wprowadzić większe zmiany:

### Wymagania
```bash
pip install mkdocs-material
```

### Kroki
```bash
# 1. Sklonuj repozytorium (lub zrób fork)
git clone https://github.com/yourusername/cmuj-wiki.git
cd cmuj-wiki

# 2. Stwórz nową gałąź
git checkout -b moje-zmiany

# 3. Edytuj pliki w folderze docs/
# (używaj swojego ulubionego edytora)

# 4. Testuj lokalnie
mkdocs serve
# Otwórz http://127.0.0.1:8000 w przeglądarce

# 5. Zatwierdź zmiany
git add .
git commit -m "Dodano materiały z biochemii"
git push origin moje-zmiany

# 6. Otwórz Pull Request na GitHubie
```

## 📝 Składnia Markdown {#skladnia-markdown}

Markdown to prosty język do formatowania tekstu. Oto podstawy:

### Nagłówki
```markdown
# Nagłówek 1
## Nagłówek 2
### Nagłówek 3
```

### Formatowanie tekstu
```markdown
**Pogrubienie**
*Kursywa*
~~Przekreślenie~~
`Kod`
```

### Listy
```markdown
- Pozycja 1
- Pozycja 2
  - Podpozycja

1. Pierwszy
2. Drugi
3. Trzeci
```

### Linki
```markdown
[Tekst linku](https://example.com)
[Link do innej strony](rok-1/anatomia.md)
```

### Cytaty i uwagi
```markdown
!!! note "Tytuł"
    Treść uwagi

!!! tip "Wskazówka"
    Przydatna wskazówka dla studentów

!!! warning "Uwaga"
    Ważna informacja

!!! success "Sukces"
    Pozytywna informacja
```

### Tabele
```markdown
| Nagłówek 1 | Nagłówek 2 |
|------------|------------|
| Komórka 1  | Komórka 2  |
| Komórka 3  | Komórka 4  |
```

### Zakładki (Tabs)
```markdown
=== "Zakładka 1"
    Treść pierwszej zakładki

=== "Zakładka 2"
    Treść drugiej zakładki
```

## 📄 Szablon strony przedmiotu

Kopiuj i wypełnij ten szablon dla nowego przedmiotu:

```markdown
# Nazwa Przedmiotu

## 📋 Informacje ogólne

- **Prowadzący**: [Dr Jan Kowalski](../prowadzacy/jan-kowalski.md)
- **ECTS**: 5
- **Rok/Semestr**: Rok II, Semestr 3

## 📚 Materiały

### Literatura

- **Główny podręcznik**: Autor - "Tytuł", wydanie
- **Dodatkowe**: Inne pozycje

### Wykłady

#### 2024/2025
- [Wykład 1 - Wprowadzenie](link-do-slajdów)
- [Wykład 2 - Temat](link-do-slajdów)

#### 2023/2024 (archiwum)
- [Wszystkie wykłady 2023/2024](link-do-folderu)

### Ćwiczenia/Seminaria

- [Materiały do ćwiczeń](link)
- [Zadania do rozwiązania](link)

### Egzaminy

#### Pytania egzaminacyjne
- [Egzamin 2024](link)
- [Egzamin 2023 z odpowiedziami](link)

### Kolokwia

- **Dr Kowalski - Grupa A**: [Kolokwium 1](link), [Kolokwium 2](link)
- **Dr Nowak - Grupa B**: [Materiały](link)

## 💬 Komentarze studentów

!!! tip "Wskazówki z roku 2024"
    - Najważniejsze są wykłady 3, 5, i 7
    - Dobrze przeczytać rozdział 10 z podręcznika
    - Kolokwia są łatwiejsze niż egzamin

!!! note "Powtórzenie z poprzednich lat"
    Na egzaminie często pojawiają się pytania z...

## 🔗 Przydatne linki

- [Oficjalny sylabus](https://sylabus.cm-uj.krakow.pl/...)
- [Strona katedry](https://...)
- [Dodatkowe materiały online](https://...)
```

## ✅ Co warto dodawać?

### Materiały
- ✅ Slajdy z wykładów (ze zgodą prowadzącego)
- ✅ Pytania egzaminacyjne z ubiegłych lat
- ✅ Własne notatki (jeśli są dobre!)
- ✅ Linki do wartościowych źródeł
- ✅ Rozwiązania zadań

### Komentarze
- ✅ Wskazówki dotyczące egzaminu
- ✅ Co jest najważniejsze w przedmiocie
- ✅ Polecane źródła do nauki
- ✅ Rzeczowa opinia o prowadzącym

### NIE dodawaj
- ❌ Materiałów chronionych prawami autorskimi (bez zgody)
- ❌ Obraźliwych komentarzy
- ❌ Informacji osobistych
- ❌ Spamu

## 🏷️ Dobre praktyki

1. **Sprawdź, czy materiał już nie istnieje** - użyj wyszukiwarki
2. **Nadawaj opisowe nazwy** - zamiast "dokument.pdf" użyj "anatomia-wykład-5-układ-nerwowy.pdf"
3. **Organizuj logicznie** - materiały według kolejności wykładów
4. **Aktualizuj daty** - zaznacz rok akademicki (np. "2024/2025")
5. **Dodaj kontekst** - krótki opis, co zawiera dany materiał

## 📁 Gdzie przechowywać duże pliki?

Wiki nie przechowuje bezpośrednio dużych plików (PDF, wideo). Zamiast tego:

1. **Google Drive** - prześlij na [medbox](https://drive.google.com/drive/folders/1SpFEsQDlYYFfqb4o5AEM0aGhNiRsWlTN)
2. **Ustaw uprawnienia** - "Każdy, kto ma link, może wyświetlać"
3. **Skopiuj link** i wklej go na wiki

## 🤝 Proces zatwierdzania zmian

1. **Wysyłasz propozycję** (Pull Request)
2. **Inni sprawdzają** - zwykle w ciągu 24-48 godzin
3. **Jeśli wszystko OK** - zmiany trafiają na stronę
4. **Jeśli są uwagi** - dostaniesz komentarz z prośbą o poprawki

## ❓ Pytania?

- 💬 **Dyskusje ogólne**: [GitHub Discussions](https://github.com/yourusername/cmuj-wiki/discussions)
- 🐛 **Zgłoś błąd**: [GitHub Issues](https://github.com/yourusername/cmuj-wiki/issues)
- 📧 **Kontakt**: [e-mail do adminów]

---

**Dziękujemy za Twój wkład w rozwój CMUJ Wiki!** 🎉

Każda zmiana, nawet najmniejsza, ma znaczenie. Razem tworzymy najlepsze źródło wiedzy dla studentów medycyny!
