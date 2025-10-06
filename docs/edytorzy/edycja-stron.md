# 📝 Jak edytować strony przedmiotów

Przewodnik po dodawaniu i edytowaniu treści na stronach przedmiotów w CMUJ Wiki.

---

## 🎯 Czego potrzebujesz?

- ✅ Konto GitHub (darmowe - [zarejestruj się tutaj](https://github.com/signup))
- ✅ Przeglądarka internetowa
- ✅ ~5-10 minut czasu

!!! tip "Najważniejsza zasada"
    **Nie musisz znać programowania!** Strony są pisane w prostym formacie Markdown - zwykły tekst z kilkoma znacznikami formatowania.

---

## 🚀 Szybki start - edycja przez GitHuba

### Krok 1: Znajdź stronę do edycji

1. Przejdź na stronę przedmiotu, którą chcesz edytować (np. Anatomia, Biochemia)
2. Kliknij ikonę **✏️** (ołówek) w prawym górnym rogu strony
3. Zostaniesz przekierowany na GitHub do edycji pliku

**LUB**

1. Wejdź na: [https://github.com/cmuj-wiki/cmuj-wiki](https://github.com/cmuj-wiki/cmuj-wiki)
2. Przejdź do folderu `docs` → `semestr-X` (gdzie X to numer semestru)
3. Kliknij na plik przedmiotu (np. `anatomia.md`, `biochemia.md`)
4. Kliknij ikonę **✏️** (Edit this file) w prawym górnym rogu

### Krok 2: Edytuj treść

Teraz możesz edytować tekst bezpośrednio w przeglądarce!

#### Podstawy formatowania Markdown:

```markdown
# Nagłówek poziomu 1
## Nagłówek poziomu 2
### Nagłówek poziomu 3

**Pogrubienie**
*Kursywa*

- Punkt listy
- Kolejny punkt

1. Numerowana lista
2. Kolejny punkt

[Tekst linku](https://adres-strony.pl)

> Cytat lub notatka
```

#### Struktura strony przedmiotu:

Każda strona przedmiotu ma sekcje:

1. **Informacje ogólne** - prowadzący, ECTS, rok/semestr
2. **Materiały** - literatura, wykłady, ćwiczenia
3. **Egzaminy** - pytania egzaminacyjne, zakres
4. **Kolokwia** - materiały do kolokwiów
5. **Komentarze studentów** - wskazówki i porady
6. **Przydatne linki** - dodatkowe zasoby

### Krok 3: Zapisz zmiany

1. Przewiń na dół strony
2. W sekcji **"Commit changes"**:
   - Dodaj krótki opis zmiany (np. `"Dodano linki do wykładów z anatomii"`)
   - Opcjonalnie: dodaj dłuższy opis w drugim polu
3. Kliknij zielony przycisk **"Commit changes"**

!!! success "Gotowe!"
    Twoje zmiany pojawią się na stronie w ciągu kilku minut!

---

## 📖 Przykłady częstych edycji

### Dodanie linku do materiałów

```markdown
### Wykłady

#### 2024/2025
- [Wykład 1 - Osteologia](https://drive.google.com/...)
- [Wykład 2 - Artrologia](https://drive.google.com/...)
```

### Dodanie polecanych książek

```markdown
### Literatura

!!! note "Polecane podręczniki"
    - **Anatomia człowieka** - Bochenek, Reicher (najlepsza polska pozycja)
    - **Sobotta - Atlas anatomii człowieka**
    - **Netter - Atlas anatomii człowieka** (bardziej przystępny)
```

### Dodanie wskazówek dla studentów

```markdown
## 💬 Komentarze studentów

!!! tip "Wskazówki do nauki"
    - Zacznij naukę od atlasów - zrozumienie struktury jest kluczowe
    - Rób notatki podczas prosektorium
    - Powtarzaj regularnie - anatomia wymaga systematyczności
    - Dołącz do grupy nauki - wspólne omawianie preparatów pomaga
```

### Dodanie informacji o kolokwium

```markdown
## Kolokwia

### Kolokwium 1 - Osteologia
- **Termin**: 15.11.2024
- **Zakres**: Kości kończyny górnej i dolnej
- **Format**: Pisemny + ustny
- **Materiały**:
  - [Pytania z ubiegłych lat](../kolokwia/semestr-1/anatomia-kol-1.html)
  - [Schemat kości](https://drive.google.com/...)
```

### Dodanie linku do quizu

Jeśli utworzyłeś quiz dla tego przedmiotu (patrz [przewodnik po quizach](../testy/quizzes/README.md)):

```markdown
## 🎯 Sprawdź swoją wiedzę

[🎯 Rozwiąż quiz z osteologii](../testy/sesja.html?quiz=anatomia-osteologia){: .md-button}
```

### Dodanie bloku z ostrzeżeniem

```markdown
!!! warning "Ważne!"
    Kolokwium obejmuje także preparaty z prosektorium - nie tylko teorię!

!!! danger "Uwaga!"
    Bez zaliczenia kolokwium 1 nie możesz podejść do egzaminu!

!!! info "Informacja"
    Materiały z wykładów znajdują się na platformie Pegaz.

!!! success "Pro tip"
    Ta metoda nauki sprawdziła się u 90% studentów!
```

---

## 🎨 Zaawansowane formatowanie

### Tworzenie tabel

```markdown
| Kolokwium | Termin | Zakres |
|-----------|--------|--------|
| Kol. 1 | 15.11 | Osteologia |
| Kol. 2 | 10.12 | Mięśnie |
| Kol. 3 | 20.01 | Układ nerwowy |
```

Wynik:

| Kolokwium | Termin | Zakres |
|-----------|--------|--------|
| Kol. 1 | 15.11 | Osteologia |
| Kol. 2 | 10.12 | Mięśnie |
| Kol. 3 | 20.01 | Układ nerwowy |

### Tworzenie zakładek

```markdown
=== "Tab 1"
    Treść pierwszej zakładki

=== "Tab 2"
    Treść drugiej zakładki
```

### Bloki kodu

```markdown
    ```python
    def hello():
        print("Hello, world!")
    ```
```

---

## 🔗 Linkowanie między stronami

### Link do innego przedmiotu

```markdown
Patrz też: [Biochemia](biochemia.html)
```

### Link do sekcji kolokwia

```markdown
Sprawdź [materiały do kolokwium](../kolokwia/semestr-1/anatomia-kol-1.html)
```

### Link do kalendarza

```markdown
[Zobacz plan zajęć](../kalendarz/index.html)
```

### Link do testów

```markdown
[Rozwiąż testy z anatomii](../testy/index.html)
```

---

## ✅ Checklist przed zapisaniem zmian

Przed zatwierdzeniem upewnij się, że:

- [ ] Sprawdziłeś/aś pisownię i gramatykę
- [ ] Linki działają poprawnie
- [ ] Formatowanie wygląda dobrze (możesz użyć zakładki "Preview")
- [ ] Dodałeś/aś jasny opis zmiany w commit message
- [ ] Informacje są aktualne i zgodne z programem zajęć

---

## 🆕 Tworzenie nowej strony przedmiotu

Jeśli przedmiot nie ma jeszcze strony:

### Krok 1: Skopiuj szablon

Najłatwiej skopiować istniejącą stronę przedmiotu i dostosować:

1. Wejdź na GitHub do folderu semestru: `docs/semestr-X/`
2. Kliknij **"Add file"** → **"Create new file"**
3. Nazwij plik: `nazwa-przedmiotu.md` (małe litery, myślniki zamiast spacji)
4. Skopiuj poniższy szablon:

```markdown
# Nazwa Przedmiotu

## 📋 Informacje ogólne

- **Prowadzący**: [Lista prowadzących](../prowadzacy/index.md)
- **ECTS**: (do uzupełnienia)
- **Rok/Semestr**: Rok X, Semestr Y

## 📚 Materiały

### Literatura

!!! note "Polecane podręczniki"
    (Do uzupełnienia - dodaj polecane książki i skrypty)

### Wykłady

#### 2024/2025
(Do uzupełnienia - dodaj linki do wykładów)

### Ćwiczenia/Seminaria

(Do uzupełnienia - dodaj materiały do ćwiczeń)

## 💬 Komentarze studentów

!!! tip "Wskazówki"
    (Do uzupełnienia - podziel się wskazówkami dla młodszych roczników)

## 🔗 Przydatne linki

- [Oficjalny sylabus UJ CM](https://sylabus.cm-uj.krakow.pl/)
- [Strona wydziału](https://wl.cm.uj.edu.pl/)

---

*Pomóż rozwijać tę stronę! Kliknij ikonę ✏️ w prawym górnym rogu, aby dodać materiały.*
```

### Krok 2: Dodaj do nawigacji

Edytuj plik `mkdocs.yml` w głównym katalogu i dodaj link do nowej strony w sekcji odpowiedniego semestru:

```yaml
  - Studia:
    - Semestr III:
      - semestr-3/index.md
      - Biofizyka: semestr-3/biofizyka.md
      - Twój nowy przedmiot: semestr-3/nazwa-przedmiotu.md  # ← DODAJ TUTAJ
```

---

## ❓ FAQ

??? question "Czy mogę dodać swoje notatki?"
    Tak! Zachęcamy do dzielenia się notatkami, pod warunkiem że są czytelne i przydatne dla innych.

??? question "Co jeśli zrobię błąd?"
    Nie martw się! Każda zmiana jest zapisywana w historii. Można ją łatwo cofnąć.

??? question "Czy mogę dodawać obrazy?"
    Tak, ale wymaga to przesłania pliku do folderu `docs/assets/images/`. Skontaktuj się z maintainerami lub zapytaj na czacie grupy.

??? question "Jak często mogę edytować?"
    Tak często, jak chcesz! Każda wartościowa zmiana jest mile widziana.

??? question "Co jeśli mam pytanie o formatowanie?"
    - Sprawdź [oficjalną dokumentację Markdown](https://www.markdownguide.org/basic-syntax/)
    - Zapytaj na czacie grupy
    - Zobacz jak zrobili to inni (otwórz inny plik `.md` i zobacz kod)

---

## 🆘 Potrzebujesz pomocy?

- 💬 Napisz na czacie grupy
- 🐛 Zgłoś problem: [GitHub Issues](https://github.com/cmuj-wiki/cmuj-wiki/issues)
- 📖 Pełna dokumentacja Markdown: [markdownguide.org](https://www.markdownguide.org/)
- 📧 Skontaktuj się z maintainerami projektu

---

*Dziękujemy za pomoc w rozwijaniu CMUJ Wiki! Każdy dodany materiał pomaga setkom studentów! 🙏*
