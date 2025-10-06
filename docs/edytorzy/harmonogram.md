# 📅 Jak zaktualizować harmonogram zajęć

Przewodnik po aktualizacji planu zajęć (harmonogramu) w CMUJ Wiki. Harmonogram aktualizuje się zazwyczaj **dwa razy w roku** (semestr zimowy i letni).

---

## 🎯 Czego potrzebujesz?

- ✅ Konto GitHub (darmowe - [zarejestruj się tutaj](https://github.com/signup))
- ✅ Przeglądarka internetowa
- ✅ Nowy harmonogram z katedry (strona katedry lub PDF)
- ✅ ~20-30 minut czasu

---

## 📋 Przegląd procesu

```
Pobierz aktualny plik → Edytuj w narzędziu → Wygeneruj JSON → Wklej w GitHubie
```

!!! tip "Rekomendowane podejście"
    Użyj **Edytora harmonogramu** - to najprostszy i najbezpieczniejszy sposób. Narzędzie automatycznie sprawdza poprawność danych!

---

## 🔧 Metoda 1: Edytor harmonogramu (REKOMENDOWANE)

### Krok 1: Pobierz aktualny plik z GitHuba

1. Wejdź na: [https://github.com/cmuj-wiki/cmuj-wiki](https://github.com/cmuj-wiki/cmuj-wiki)
2. Przejdź do folderu: `docs` → `static` → `schedule_data_v2.json`
3. Kliknij przycisk **"Download raw file"** (ikona pobierania) lub **"Raw"** i zapisz plik

### Krok 2: Otwórz edytor harmonogramu

[🔧 Otwórz Edytor Harmonogramu](../schedule-editor.html){: .md-button .md-button--primary target="_blank"}

### Krok 3: Wczytaj plik do edytora

1. Kliknij przycisk **"📂 Wczytaj JSON"**
2. Wybierz pobrany plik `schedule_data_v2.json`
3. Tabela wypełni się danymi

### Krok 4: Edytuj zajęcia

Teraz możesz:

- **Kliknąć w komórkę** aby edytować wartość
- **Dodać nowe zajęcia** przyciskiem "➕ Dodaj zajęcia"
- **Usunąć zajęcia** przyciskiem "×" w ostatniej kolumnie

#### Znaczenie kolumn:

| Kolumna | Opis | Przykład |
|---------|------|----------|
| **Grupa** | Numer grupy (1-20) | `1`, `2`, `15` |
| **Dzień** | Dzień tygodnia (0=Pon, 6=Niedz) | `0` (Pon), `4` (Pt) |
| **Nazwa dnia** | Pełna nazwa (opcjonalna) | `Poniedziałek` |
| **Godz.** | Godzina rozpoczęcia (0-23) | `8`, `14` |
| **Min.** | Minuta rozpoczęcia (0-59) | `0`, `15`, `30` |
| **Czas [min]** | Długość zajęć w minutach | `90`, `180` |
| **Przedmiot** | Nazwa przedmiotu | `Anatomia`, `Biochemia ćw.` |
| **Typ** | Typ zajęć (opcjonalne) | `Wykład`, `Seminarium` |
| **Lokalizacja** | Miejsce zajęć | `ul. Kopernika 7` |
| **Daty** | Ograniczenia dat (patrz niżej) | `do 7.XI`, `28.XI - 16.I` |

#### Format dat:

Pole "Daty" określa, kiedy zajęcia się odbywają:

- **Puste** - zajęcia przez cały semestr
- **`do 7.XI`** - zajęcia tylko do 7 listopada
- **`28.XI - 16.I`** - zajęcia od 28 listopada do 16 stycznia
- **`15.X`** - zajęcia tylko 15 października

!!! info "Liczby rzymskie dla miesięcy"
    Używaj rzymskich cyfr dla miesięcy: I (styczeń), II (luty), III (marzec), IV (kwiecień), V (maj), VI (czerwiec), VII (lipiec), VIII (sierpień), IX (wrzesień), X (październik), XI (listopad), XII (grudzień)

### Krok 5: Wygeneruj JSON

1. Kliknij **"✅ Generuj i kopiuj JSON"**
2. Narzędzie sprawdzi poprawność danych:
   - ✅ **Sukces** - JSON skopiowany do schowka automatycznie!
   - ❌ **Błąd** - zobacz komunikaty błędów i popraw dane

### Krok 6: Wklej w GitHubie

1. Wróć do [schedule_data_v2.json na GitHubie](https://github.com/cmuj-wiki/cmuj-wiki/blob/main/docs/static/schedule_data_v2.json)
2. Kliknij przycisk **✏️ Edit** (ołówek w prawym górnym rogu)
3. **Zaznacz całą zawartość** (Ctrl+A / Cmd+A) i **usuń**
4. **Wklej** nowy JSON ze schowka (Ctrl+V / Cmd+V)
5. Przewiń na dół i kliknij **"Commit changes"**
6. Dodaj opis zmiany, np. `"Aktualizacja harmonogramu - semestr zimowy 2025/2026"`
7. Kliknij **"Commit changes"** (zielony przycisk)

!!! success "Gotowe!"
    Twoje zmiany zostaną automatycznie sprawdzone i pojawią się na stronie w ciągu kilku minut!

---

## 💡 Metoda 2: Szybkie dodawanie z pomocą ChatGPT (OPCJONALNE)

Jeśli zaczynasz od nowa i masz dostęp do ChatGPT, możesz użyć go do wygenerowania **wstępnej wersji** danych, którą potem zweryfikujesz w edytorze.

### Krok 1: Skopiuj harmonogram z katedry

1. Znajdź harmonogram na stronie katedry lub w PDF
2. **Zaznacz całą tabelę** i skopiuj (Ctrl+C / Cmd+C)

### Krok 2: Użyj ChatGPT

Wklej do ChatGPT następujący prompt:

```
Przekształć poniższą tabelę harmonogramu zajęć na format CSV z kolumnami:
group,day,day_name,hour,minute,duration,subject,type,location,dates

Zasady:
- day: 0=Poniedziałek, 1=Wtorek, 2=Środa, 3=Czwartek, 4=Piątek
- duration: czas w minutach
- dates: puste JEŚLI zajęcia przez cały semestr, w przeciwnym razie "do DD.MM" lub "DD.MM - DD.MM" z RZYMSKIMI cyframi dla miesięcy (I-XII)
- Jeśli pole jest puste, wpisz puste (bez wartości między przecinkami)

Przykład:
1,0,Poniedziałek,8,15,90,Anatomia,Wykład,ul. Kopernika 7,
2,0,Poniedziałek,10,30,180,Biochemia ćw.,,ul. Kopernika 7,do 7.XI

Oto tabela:
[WKLEJ TUTAJ SKOPIOWANĄ TABELĘ]
```

### Krok 3: Zaimportuj CSV do edytora

1. Skopiuj wygenerowany CSV od ChatGPT
2. Otwórz Excel lub Google Sheets
3. Wklej CSV i zapisz jako plik `.csv`
4. W przyszłości edytor będzie wspierać import CSV bezpośrednio (na razie przekonwertuj ręcznie lub użyj narzędzia online)

!!! warning "Ważne: Zawsze weryfikuj!"
    ChatGPT może popełniać błędy! **Zawsze** sprawdź wygenerowane dane w edytorze harmonogramu przed wysłaniem do GitHuba.

---

## ✅ Checklist przed zatwierdzeniem

Przed wysłaniem zmian upewnij się, że:

- [ ] Wszystkie grupy (1-20) mają poprawne zajęcia
- [ ] Godziny są w formacie 24h (np. 14:15, nie 2:15 PM)
- [ ] Daty używają liczb rzymskich (XI, nie 11)
- [ ] Nazwy przedmiotów są spójne (np. zawsze "Anatomia", nie raz "Anat.")
- [ ] Lokalizacje są kompletne
- [ ] Edytor pokazał **✅ Sukces** przy generowaniu JSON

---

## 🔗 Linkowanie harmonogramu do strony przedmiotu

Po zaktualizowaniu harmonogramu możesz dodać link do niego na stronie przedmiotu:

### Przykład dla przedmiotu Biochemia

Edytuj plik `docs/semestr-1/biochemia.md` i dodaj:

```markdown
## 📅 Plan zajęć

[Zobacz plan zajęć w kalendarzu](../kalendarz/index.html){: .md-button}

Zajęcia z biochemii odbywają się:
- **Wykłady**: Poniedziałki, 8:15-9:45, ul. Kopernika 7
- **Ćwiczenia**: Środy, 10:30-13:30 (według grupy)
```

---

## ❓ FAQ

??? question "Co zrobić gdy harmonogram się zmienia w trakcie semestru?"
    Powtórz proces - pobierz aktualny plik, wprowadź zmiany w edytorze, wyślij nowy JSON.

??? question "Czy mogę edytować tylko jedną grupę?"
    Tak! Wczytaj pełny plik, edytuj tylko zajęcia dla swojej grupy, wyślij cały plik z powrotem.

??? question "Co jeśli edytor zgłasza błędy?"
    Przeczytaj komunikaty błędów - wskazują dokładnie, co jest nie tak (np. "Grupa musi być 1-20", "Godzina musi być 0-23"). Popraw wartości i spróbuj ponownie.

??? question "Czy zmiany są natychmiastowe?"
    GitHub automatycznie buduje stronę po zatwierdzeniu zmian. Proces trwa ~3-5 minut.

??? question "Co jeśli przypadkowo coś zepsuję?"
    Nie martw się! GitHub ma automatyczną walidację - jeśli dane są niepoprawne, Twój commit zostanie odrzucony z wyraźnym komunikatem błędu. Strona się nie zepsuje.

---

## 🆘 Potrzebujesz pomocy?

- 💬 Napisz na czacie grupy
- 🐛 Zgłoś problem: [GitHub Issues](https://github.com/cmuj-wiki/cmuj-wiki/issues)
- 📧 Skontaktuj się z maintainerami projektu

---

*Dziękujemy za pomoc w utrzymywaniu aktualnego harmonogramu! 🙏*
