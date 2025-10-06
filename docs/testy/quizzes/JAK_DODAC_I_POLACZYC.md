# 🔗 Jak dodać quiz i połączyć go ze stroną przedmiotu

> **Kompletna instrukcja:** Od stworzenia quizu do linkowania na stronie przedmiotu

---

## 📝 Krok 1: Stwórz plik quizu

### Gdzie umieścić plik?

**Zawsze w folderze:** `docs/testy/quizzes/`

### Jak nazwać plik?

**Format:** `przedmiot-temat.md`

**Przykłady:**
- `etyka-kazusy-medyczne.md`
- `fizjologia-uklad-krazenia.md`
- `farmakologia-antybiotyki.md`
- `anatomia-neuroanatomia.md`

!!! warning "Ważne!"
    - Używaj małych liter
    - Zamiast spacji używaj myślnika `-`
    - Rozszerzenie `.md` jest obowiązkowe
    - Nie używaj polskich znaków w nazwie (ą, ę, ć, etc.)

### Jak stworzyć quiz?

1. **Skopiuj szablon:**
   - Otwórz plik `docs/testy/quizzes/_TEMPLATE.md`
   - Kliknij "Copy raw file" lub skopiuj zawartość

2. **Utwórz nowy plik:**
   - W GitHubie przejdź do `docs/testy/quizzes/`
   - Kliknij **"Add file"** → **"Create new file"**
   - Nazwij: np. `etyka-kazusy-medyczne.md`

3. **Wklej szablon i edytuj:**

```markdown
# Etyka w medycynie - Kazusy medyczne

Quiz sprawdzający znajomość dylematów etycznych w praktyce lekarskiej.

## Czy lekarz może ujawnić informacje o pacjencie rodzinie bez zgody pacjenta?

- [ ] Tak, zawsze
- [x] Nie, tylko w wyjątkowych przypadkach
- [ ] Tak, jeśli rodzina pyta
- [ ] Tylko jeśli pacjent jest nieprzytomny

> Lekarz objęty jest tajemnicą lekarską. Może ją ujawnić tylko w przypadkach określonych prawem.

## Jakie zasady obowiązują przy świadomej zgodzie pacjenta?

- [x] Pacjent musi być poinformowany o ryzyku
- [x] Zgoda musi być dobrowolna
- [x] Pacjent ma prawo do odmowy
- [ ] Lekarz może zignorować odmowę

> Świadoma zgoda wymaga: pełnej informacji, dobrowolności i prawa do odmowy.
```

4. **Zapisz (Commit):**
   - Scroll na dół
   - Wpisz opis: "Dodano quiz z etyki - kazusy medyczne"
   - Kliknij **"Commit changes"**

---

## 🔗 Krok 2: Połącz quiz ze stroną przedmiotu

### Scenariusz A: Linkowanie z głównej strony przedmiotu

**Przykład:** Chcesz dodać quiz do strony etyki

1. **Znajdź stronę przedmiotu:**
   - Sprawdź gdzie jest strona etyki, np. `docs/semestr-X/etyka.md`

2. **Kliknij ikonę ołówka** (Edit this file)

3. **Dodaj sekcję z quizami** (jeśli nie ma):

```markdown
## 📝 Quizy - sprawdź się!

### Kazusy medyczne

Przećwicz rozwiązywanie dylematów etycznych na przykładach z praktyki.

[🎯 Rozwiąż quiz](../testy/sesja.html?quiz=etyka-kazusy-medyczne){: .md-button .md-button--primary}

---
```

**Wyjaśnienie URL:**
- `../testy/sesja.html` - ścieżka do strony sesji testowej
- `?quiz=etyka-kazusy-medyczne` - nazwa twojego quizu (bez `.md`)
- Nazwa quizu = nazwa pliku bez rozszerzenia

### Scenariusz B: Dodanie do istniejącej sekcji quizów

Jeśli strona już ma sekcję "Quizy" lub "Testy", po prostu dodaj:

```markdown
### Kazusy medyczne

Dylematy etyczne w praktyce lekarskiej.

[🎯 Rozwiąż quiz](../testy/sesja.html?quiz=etyka-kazusy-medyczne){: .md-button}
```

### Scenariusz C: Lista wielu quizów

```markdown
## 📝 Dostępne quizy

<div class="quiz-grid">
    <div class="quiz-card">
        <h3>Kazusy medyczne</h3>
        <p>Dylematy etyczne w praktyce lekarskiej</p>
        <a href="../testy/sesja.html?quiz=etyka-kazusy-medyczne" class="quiz-start-btn">
            ▶️ Rozpocznij test
        </a>
    </div>

    <div class="quiz-card">
        <h3>Kodeks etyki lekarskiej</h3>
        <p>Podstawowe zasady i przepisy</p>
        <a href="../testy/sesja.html?quiz=etyka-kodeks" class="quiz-start-btn">
            ▶️ Rozpocznij test
        </a>
    </div>
</div>
```

---

## 📍 Krok 3: Jak zbudować poprawny URL?

### Wzór:

```
../testy/sesja.html?quiz=NAZWA-PLIKU-BEZ-MD
```

### Przykłady:

| Plik quizu | URL w linku |
|------------|-------------|
| `etyka-kazusy-medyczne.md` | `../testy/sesja.html?quiz=etyka-kazusy-medyczne` |
| `fizjologia-serce.md` | `../testy/sesja.html?quiz=fizjologia-serce` |
| `anatomia-kosci.md` | `../testy/sesja.html?quiz=anatomia-kosci` |

### Dlaczego `../testy/`?

- Strona przedmiotu jest w: `docs/semestr-X/przedmiot.md`
- Quiz jest dostępny pod: `docs/testy/sesja.html`
- `..` = wyjdź z folderu `semestr-X` do `docs`
- Następnie wejdź do `testy/`

---

## ✅ Checklist: Dodawanie quizu + linkowanie

### Tworzenie quizu:
- [ ] Skopiowałem szablon `_TEMPLATE.md`
- [ ] Stworzyłem plik w `docs/testy/quizzes/`
- [ ] Nazwa pliku: małe litery, bez spacji (używam `-`)
- [ ] Dodałem pytania z `[x]` dla poprawnych odpowiedzi
- [ ] Każde pytanie ma wyjaśnienie (`> Wyjaśnienie...`)
- [ ] Commitowałem zmiany

### Linkowanie:
- [ ] Znalazłem stronę przedmiotu (`docs/semestr-X/przedmiot.md`)
- [ ] Dodałem sekcję "Quizy" (jeśli nie było)
- [ ] Utworzyłem link: `../testy/sesja.html?quiz=NAZWA-PLIKU`
- [ ] Sprawdziłem, czy nazwa quizu = nazwa pliku bez `.md`
- [ ] Commitowałem zmiany

---

## 🎯 Pełny przykład: Quiz z etyki

### 1. Tworzę plik quizu

**Lokalizacja:** `docs/testy/quizzes/etyka-kazusy.md`

```markdown
# Etyka w medycynie - Kazusy praktyczne

## Pacjent odmawia transfuzji z powodów religijnych. Co robisz?

- [ ] Wykonuję transfuzję mimo odmowy
- [x] Szukam alternatywnych metod leczenia
- [ ] Informuję rodzinę, żeby przekonała pacjenta
- [x] Dokumentuję odmowę i jej konsekwencje

> Należy poszukać alternatyw i udokumentować świadomą odmowę pacjenta.

## Pacjent ma prawo do:

- [x] Dostępu do dokumentacji medycznej
- [x] Informacji o rozpoznaniu
- [x] Odmowy leczenia
- [ ] Żądania konkretnego leku

> Pacjent ma prawo do informacji i odmowy, ale nie może żądać konkretnych leków.
```

**Commit:** "Dodano quiz z etyki - kazusy praktyczne"

### 2. Linkuję na stronie etyki

**Edytuję plik:** `docs/semestr-1/etyka.md` (lub gdzie jest strona etyki)

**Dodaję na końcu:**

```markdown
---

## 📝 Sprawdź swoją wiedzę

### Kazusy praktyczne

Test sprawdzający umiejętność rozwiązywania dylematów etycznych w praktyce.

**Poziom:** podstawowy | **Pytania:** 10 | **Czas:** ~10 min

[🎯 Rozpocznij quiz](../testy/sesja.html?quiz=etyka-kazusy){: .md-button .md-button--primary}
```

**Commit:** "Dodano link do quizu z etyki"

### 3. Gotowe!

Quiz pojawi się automatycznie po zbudowaniu strony.

---

## 🔍 Jak sprawdzić, czy działa?

### Lokalnie (opcjonalnie):

```bash
mkdocs build
mkdocs serve
```

Odwiedź: `http://localhost:8000/semestr-X/etyka.html`

Kliknij link do quizu → powinien się załadować!

### Po deploymencie:

1. Otwórz stronę przedmiotu
2. Kliknij link do quizu
3. Sprawdź czy quiz się ładuje

Jeśli widzisz "Quiz not found" → sprawdź nazwę w URL!

---

## 🐛 Najczęstsze problemy

### "Quiz not found"

**Przyczyna:** Nazwa w URL nie zgadza się z nazwą pliku

**Sprawdź:**
- Plik: `etyka-kazusy-medyczne.md`
- URL musi być: `?quiz=etyka-kazusy-medyczne`

### Link nie działa

**Przyczyna:** Zła ścieżka względna

**Z poziomu:**
- `docs/semestr-1/etyka.md` używaj: `../testy/sesja.html?quiz=...`
- `docs/testy/index.md` używaj: `sesja.html?quiz=...`

### Quiz się nie kompiluje

**Sprawdź:**
```bash
python3 scripts/validate_quizzes.py docs/testy/quizzes/twoj-quiz.md
```

Poprawi błędy wskazane w komunikacie.

---

## 💡 Szybkie wzory do skopiowania

### Prosty przycisk:

```markdown
[🎯 Rozwiąż quiz](../testy/sesja.html?quiz=NAZWA-QUIZU){: .md-button}
```

### Większy przycisk (primary):

```markdown
[🎯 Rozwiąż quiz](../testy/sesja.html?quiz=NAZWA-QUIZU){: .md-button .md-button--primary}
```

### Kartka z opisem:

```markdown
!!! tip "Test z etyki"
    Sprawdź swoją znajomość kazusów medycznych.

    **📝 10 pytań | ⏱️ ~10 min**

    [Rozpocznij quiz](../testy/sesja.html?quiz=etyka-kazusy){: .md-button}
```

### Lista quizów:

```markdown
## Dostępne quizy

- [Kazusy medyczne](../testy/sesja.html?quiz=etyka-kazusy) - dylematy etyczne
- [Kodeks etyki](../testy/sesja.html?quiz=etyka-kodeks) - zasady zawodowe
- [Zgoda pacjenta](../testy/sesja.html?quiz=etyka-zgoda) - informed consent
```

---

## 📚 Więcej przykładów

Zobacz jak to zrobiono w:
- [docs/testy/index.md](../index.md) - lista wszystkich quizów
- [docs/semestr-1/anatomia.md] - przykład linkowania (jeśli istnieje)

---

## ❓ FAQ - Linkowanie

**Q: Czy muszę dodawać quiz do index.md?**
A: Nie jest wymagane, ale warto - wtedy pojawi się na głównej liście testów.

**Q: Czy mogę linkować quiz z wielu miejsc?**
A: Tak! Ten sam quiz można linkować z kilku stron przedmiotów.

**Q: Jak zmienić nazwę quizu po utworzeniu?**
A: Zmień nazwę pliku .md I zaktualizuj wszystkie linki.

**Q: Co jeśli mój quiz ma obrazki?**
A: Linkowanie jest takie samo! System automatycznie wykryje typ quizu.

**Q: Czy quiz od razu pojawi się na stronie?**
A: Po commitcie GitHub zbuduje stronę (2-3 min). Potem odśwież przeglądarkę.

---

## 🆘 Potrzebujesz pomocy?

1. **Sprawdź przykłady** - `anatomia-osteologia.md`, `biochemia-bialka.md`
2. **Uruchom walidację** - `python3 scripts/validate_quizzes.py`
3. **Zobacz logi buildu** - GitHub Actions pokaże błędy
4. **Zapytaj na czacie** - ktoś na pewno pomoże!

---

**To wszystko! Teraz możesz dodać quiz i połączyć go z dowolną stroną przedmiotu** 🎉
