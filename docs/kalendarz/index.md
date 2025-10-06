# 📅 Kalendarz Zajęć

!!! success "Kalendarz v1.0 - Gotowy do użytku"
    Kalendarz został przetestowany i wszystkie znane błędy parsera zostały naprawione.
    Jeśli zauważysz jakiekolwiek problemy, zgłoś je przez GitHub Issues!

---

## 📊 Twój harmonogram

<div id="calendar-container">
    <div class="calendar-loading">⏳ Ładowanie kalendarza...</div>
</div>

---

## 🔍 Jakość danych

<div id="data-quality-panel" class="data-quality-panel">
    <!-- Will be populated by JavaScript -->
</div>

---

## 💡 Jak korzystać z kalendarza?

1. **Wybierz grupę** - jeśli nie wybrałeś jeszcze swojej grupy, zostaniesz poproszony o wybór
2. **Przeglądaj zajęcia** - zobacz wszystkie zajęcia dla swojej grupy w tym tygodniu
3. **Kliknij zajęcia** - aby zobaczyć szczegóły (lokalizacja, typ zajęć)
4. **Zgłaszaj błędy** - jeśli widzisz nieprawidłowe godziny lub konflikty

## ℹ️ Informacje dodatkowe

- **Kliknij zajęcia** - aby zobaczyć szczegóły (lokalizacja, czas trwania, daty zajęć)
- **Panel jakości danych** - zobacz statystyki kalendarza
- **🚨 Konflikty** - kalendarz automatycznie wykrywa nakładające się zajęcia

---

## ❓ FAQ

??? question "Co oznacza konflikt?"
    Konflikt to sytuacja, gdy dwa zajęcia dla tej samej grupy nakładają się czasowo.
    Kalendarz automatycznie wykrywa takie sytuacje i oznacza je czerwonym kolorem.

??? question "Jak długo trwają zajęcia?"
    Parser automatycznie wykrywa czas trwania zajęć na podstawie kolorowych bloków w pliku XLSX.
    Każda komórka to 15 minut, więc różne zajęcia mogą mieć różny czas trwania (90, 120, 135, 150 minut).

??? question "Skąd kalendarz wie, kiedy odbywają się zajęcia?"
    Niektóre zajęcia mają ograniczenia dat (np. "do 7.XI" lub "28.XI - 16.I").
    Kalendarz automatycznie filtruje zajęcia na podstawie tych dat i pokazuje tylko aktualne.

??? question "Mogę pomóc ulepszyć kalendarz?"
    Tak! Jeśli zauważysz błędne dane, zgłoś je przez GitHub Issues lub edytuj parser bezpośrednio.
    Zobacz [jak dodać materiały](../jak-edytowac.md).

---

## 🔗 Przydatne linki

- [Plan zajęć (PDF/XLSX)](../plan-zajec.html) - Oficjalny plan do pobrania
- [Kolokwia](../kolokwia/index.md) - Terminy i zakres kolokwiów
- [Homepage](../index.md) - Wróć do strony głównej

---

*✅ Kalendarz v1.0 - wszystkie dane zweryfikowane i gotowe do użytku! 🚀*
