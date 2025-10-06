# 📝 Jak dodać nowy test - Instrukcja dla edytorów

> **TL;DR:** Skopiuj `_TEMPLATE.md`, edytuj pytania, zaznacz poprawne odpowiedzi przez `[x]`, commituj. Gotowe!

---

## 🎯 Dla kogo ta instrukcja?

Jesteś studentem i chcesz dodać quiz do CMUJ Wiki? **Świetnie!** To zajmie Ci 5 minut.

Nie musisz znać się na programowaniu - wystarczy że potrafisz edytować tekst na GitHubie.

---

## 🚀 Szybki start - Test tekstowy

### Krok 1: Skopiuj szablon

1. Wejdź do folderu `docs/testy/quizzes/`
2. Skopiuj plik `_TEMPLATE.md`
3. Nazwij go opisowo, np. `fizjologia-serce.md`

### Krok 2: Edytuj w GitHubie

Kliknij **ikonę ołówka** w prawym górnym rogu (Edit this file).

### Krok 3: Napisz pytania

```markdown
# Fizjologia - Układ krążenia

Quiz o sercu i układzie krążenia.

## Ile komór ma serce człowieka?

- [ ] 2
- [ ] 3
- [x] 4
- [ ] 5

> Serce ma 4 komory: 2 przedsionki i 2 komory.

## Zaznacz wszystkie tętnice wieńcowe:

- [x] Lewa tętnica wieńcowa
- [x] Prawa tętnica wieńcowa
- [ ] Aorta
- [ ] Żyła główna górna

> Tętnice wieńcowe zaopatrują mięsień sercowy w krew.
```

### Krok 4: Zapisz i commituj

- Przewiń na dół
- Wpisz opis zmiany: "Dodano quiz z fizjologii - układ krążenia"
- Kliknij **Commit changes**

### 🎉 Gotowe!

Twój quiz pojawi się automatycznie na stronie po zbudowaniu!

---

## 🔗 Jak połączyć quiz ze stroną przedmiotu?

**Chcesz dodać link do quizu na stronie etyki, anatomii lub innego przedmiotu?**

📖 **Zobacz szczegółową instrukcję: [Jak dodać i połączyć quiz](JAK_DODAC_I_POLACZYC.md)**

### Szybka instrukcja linkowania:

1. **Stwórz quiz:** `docs/testy/quizzes/etyka-kazusy.md` ✅
2. **Edytuj stronę przedmiotu:** np. `docs/semestr-2/etyka.md` (kliknij ołówek)
3. **Dodaj link:**
   ```markdown
   [🎯 Rozwiąż quiz](../testy/sesja.html?quiz=etyka-kazusy){: .md-button}
   ```
4. **Commit!**

**Ważne:** Nazwa w URL = nazwa pliku bez `.md`

**Przykład dla etyki:**
- Plik: `etyka-kazusy-medyczne.md`
- URL: `../testy/sesja.html?quiz=etyka-kazusy-medyczne`

---

## 📖 Szczegółowe zasady

### Struktura pytania

Każde pytanie składa się z:

1. **Nagłówek** - zaczyna się od `##`
2. **Odpowiedzi** - lista z checkboxami
3. **Wyjaśnienie** - blok cytatu (opcjonalnie)

```markdown
## To jest pytanie

- [ ] Odpowiedź niepoprawna
- [x] Odpowiedź poprawna
- [ ] Inna niepoprawna

> Wyjaśnienie, dlaczego tak jest.
```

### Pojedynczy vs wielokrotny wybór

**System automatycznie rozpoznaje typ pytania:**

- **Jeden `[x]`** → pytanie jednokrotnego wyboru (radio buttons)
- **Wiele `[x]`** → pytanie wielokrotnego wyboru (checkboxy)

### Dodawanie obrazków

Możesz dodać obrazek do pytania:

```markdown
## ![](images/ekg.png) Co pokazuje ten wykres EKG?

- [ ] Tachykardia
- [x] Migotanie przedsionków
- [ ] Bradykardia

> Migotanie przedsionków charakteryzuje się...
```

Umieść obrazki w podfolderze `images/` obok pliku .md

---

## 🖼️ Test obrazkowy (szkiełka histologiczne)

### Format dla testów ze zdjęciami

1. **Stwórz folder** np. `histologia-zestaw-10/`
2. **Dodaj podfolder** `images/`
3. **Wrzuć obrazki** nazwane `1.jpg`, `2.jpg`, `3.jpg`... (kolejność liczy!)
4. **Stwórz plik** `answers.txt` z odpowiedziami

### Przykład struktury:

```
histologia-zestaw-10/
├── images/
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── 3.jpg
│   └── ...
└── answers.txt
```

### Plik `answers.txt`:

```
1. Wątroba - hepatocyty
2. Nerka - kłębuszek nerkowy
3. Płuco - pęcherzyki płucne
...
```

**Uwaga:** Liczba odpowiedzi musi = liczba obrazków!

---

## ✅ Checklist przed commitem

- [ ] Tytuł quizu jest opisowy (`# Przedmiot - Temat`)
- [ ] Każde pytanie ma co najmniej 2 odpowiedzi
- [ ] Każde pytanie ma przynajmniej jedną poprawną odpowiedź `[x]`
- [ ] Wyjaśnienia są zrozumiałe (nie trzeba ich dodawać do każdego)
- [ ] Jeśli są obrazki, są w folderze `images/`
- [ ] Sprawdziłem/am podgląd na GitHubie przed commitem

---

## 🐛 Najczęstsze błędy

### ❌ Brak poprawnej odpowiedzi

```markdown
## Pytanie bez poprawnej odpowiedzi

- [ ] A
- [ ] B
- [ ] C
```

**Błąd:** Brak `[x]`. System wyrzuci błąd podczas budowania.

### ❌ Zła składnia checkbox

```markdown
- [X] To zadziała (wielka litera X też OK)
- [x] To też zadziała ✓
- [ x] To NIE zadziała (spacja wewnątrz)
- [v] To NIE zadziała (v zamiast x)
```

### ❌ Brak pytania

```markdown
##

- [x] Odpowiedź

> Wyjaśnienie
```

**Błąd:** Puste pytanie po `##`

---

## 💡 Wskazówki

### Dobre praktyki

✅ **Konkretne pytania:**
```markdown
## Jaki hormon wydziela tarczyca?
```

✅ **Krótkie odpowiedzi:**
```markdown
- [x] Tyroksyna (T4)
```

✅ **Pomocne wyjaśnienia:**
```markdown
> Tyroksyna reguluje metabolizm. Jej niedobór powoduje niedoczynność tarczycy.
```

### Jak sprawdzić czy działa?

1. **GitHub podgląd** - checkboxy się renderują!
2. **Zbuduj lokalnie** (opcjonalnie):
   ```bash
   mkdocs build
   ```
3. **Sprawdź logi** - czy quiz się skompilował:
   ```
   ✓ Compiled quiz: twoj-quiz.md
   ```

---

## 🆘 Pomoc

### Mam problem!

1. **Przeczytaj błąd** - build pokazuje dokładnie co jest źle i w której linii
2. **Porównaj z szablonem** - `_TEMPLATE.md` zawiera przykłady
3. **Zobacz przykłady** - `anatomia-osteologia.md`, `biochemia-bialka.md`
4. **Zapytaj na czacie** - ktoś na pewno pomoże!

### Przykładowe błędy buildowania

```
Error in anatomia-kości.md: No correct answer marked for question "Ile kości..."
```
→ Dodaj `[x]` do poprawnej odpowiedzi

```
Error parsing question 5: No answers found
```
→ Brak listy odpowiedzi (zacznij od `- [ ]`)

---

## 📚 Przykłady

Gotowe przykłady quizów znajdziesz w tym folderze:

- **`anatomia-osteologia.md`** - quiz tekstowy, pytania jednokrotnego wyboru
- **`biochemia-bialka.md`** - quiz z pytaniami wielokrotnego wyboru
- **`histologia-zestaw-demo/`** - quiz obrazkowy

Możesz je otworzyć i skopiować strukturę!

---

## 🎓 Dla zaawansowanych

### GitHub Actions

Po commicie GitHub Actions automatycznie:
1. Waliduje format quizu
2. Kompiluje do JSON
3. Buduje stronę
4. Publikuje

Jeśli coś jest źle, zobaczysz błąd w PR.

### Testowanie lokalne

Jeśli chcesz przetestować lokalnie:

```bash
# Zainstaluj zależności
pip install -e .

# Zbuduj stronę
mkdocs build

# Zobacz wyjście
ls docs/assets/quiz-data/
```

### Metadane (opcjonalne)

Możesz dodać więcej info w tytule:

```markdown
# Anatomia - Osteologia

Difficulty: podstawowy
Semester: 1
Points: 10

Quiz sprawdzający...
```

System automatycznie wyciąga subject i topic z pierwszej linii `# Subject - Topic`.

---

## 📬 Feedback

Masz pomysł jak ulepszyć tę instrukcję lub system quizów?

- Napisz na czacie grupy
- Stwórz issue na GitHubie
- Edytuj ten plik i wyślij PR!

---

**Powodzenia w tworzeniu quizów! 🚀**
