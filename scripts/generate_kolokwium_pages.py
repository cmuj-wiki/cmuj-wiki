#!/usr/bin/env python3
"""
Generate kolokwium detail pages from exam_dates_manual.yml

This script reads the structured exam date data and generates
individual markdown pages for each kolokwium/exam.
"""

import yaml
import os
from pathlib import Path
from datetime import datetime

# Paths
ROOT_DIR = Path(__file__).parent.parent
DATA_FILE = ROOT_DIR / "data" / "exam_dates_manual.yml"
KOLOKWIA_DIR = ROOT_DIR / "docs" / "kolokwia" / "semestr-1"

# Subject name mapping (slug -> display name)
SUBJECT_NAMES = {
    "anatomia": "Anatomia z embriologią",
    "biochemia": "Biochemia z elementami chemii",
    "histologia": "Histologia z embriologią",
    "bhk": "Biofizyka, Hygiena, Kierunkowość",
    "etyka": "Etyka w medycynie",
    "historia_medycyny": "Historia medycyny",
    "wychowanie_fizyczne": "Wychowanie fizyczne",
}

# Polish month names for display
MONTHS_PL = [
    "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
    "lipca", "sierpnia", "września", "października", "listopada", "grudnia"
]

def format_date_polish(date_str):
    """Convert YYYY-MM-DD to Polish format: DD miesiąca YYYY"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.day} {MONTHS_PL[dt.month - 1]} {dt.year}"
    except:
        return date_str

def format_groups(groups):
    """Format group list or 'all'"""
    if groups == "all":
        return "Wszystkie grupy"
    elif isinstance(groups, list):
        if len(groups) > 4:
            return f"Grupy {groups[0]}-{groups[-1]}"
        else:
            return f"Grupy {', '.join(map(str, groups))}"
    return str(groups)

def generate_kolokwium_page(subject_slug, subject_name, event_data, event_type, event_index):
    """Generate a single kolokwium page"""

    # Create filename
    event_type_slug = event_type.replace(" ", "-").lower()
    filename = f"{subject_slug}-{event_type_slug}-{event_index}.md"
    filepath = KOLOKWIA_DIR / filename

    # Extract event data
    date = event_data.get("date", "TBD")
    time = event_data.get("time", "TBD")
    exam_type = event_data.get("type", "")
    topic = event_data.get("topic", "")
    location = event_data.get("location", "")
    groups = event_data.get("groups", [])
    note = event_data.get("note", "")
    term = event_data.get("term", "")

    # Format date
    date_formatted = format_date_polish(date)
    groups_formatted = format_groups(groups)

    # Create title
    if event_type == "kolokwia":
        title = f"{subject_name} - Kolokwium {event_index}"
    elif event_type == "egzaminy":
        title = f"{subject_name} - Egzamin"
        if term:
            title += f" ({term})"
    else:
        title = f"{subject_name} - {event_type.title()}"

    # Generate content
    content = f"""# {title}

## 📅 Informacje podstawowe

| | |
|---|---|
| **Data** | {date_formatted} |
"""

    if time and time != "TBD":
        content += f"| **Godzina** | {time} |\n"

    if exam_type:
        content += f"| **Typ** | {exam_type.title()} |\n"

    content += f"| **Grupy** | {groups_formatted} |\n"

    if location:
        content += f"| **Miejsce** | {location} |\n"

    if note:
        content += f"\n!!! info \"Uwaga\"\n    {note}\n"

    content += f"""
!!! warning "Weryfikuj termin"
    Zawsze sprawdź aktualny harmonogram na oficjalnej stronie katedry.

---

## 📋 Zakres materiału

### Temat: **{topic if topic else 'Do uzupełnienia'}**

!!! note "Do uzupełnienia"
    Szczegółowy zakres materiału będzie dostępny wkrótce.

    W międzyczasie sprawdź:
    - Oficjalny sylabus przedmiotu
    - Materiały z wykładów
    - Notatki z ćwiczeń

---

## 📚 Materiały do nauki

### Podręczniki

📥 [Zobacz zalecane podręczniki](../../semestr-1/{subject_slug}.md#literatura)

📥 [Pobierz podręczniki z MedBox](../../zasoby/medbox/semestr-1.md#{subject_slug})

### Pytania z poprzednich lat

📝 [Pytania z kolokwiów - MedBox](../../zasoby/medbox/semestr-1.md#{subject_slug})

---

## 💡 Wskazówki od studentów

!!! tip "Podziel się swoimi wskazówkami!"
    Zdałeś/zdałaś to kolokwium? Pomóż młodszym rocznikom!

    [Edytuj tę stronę](https://github.com/yourusername/cmuj-wiki/edit/main/docs/kolokwia/semestr-1/{filename})

### Jak się przygotować?

*(Do uzupełnienia przez studentów)*

- Wskazówki dotyczące formatu egzaminu
- Na co zwrócić uwagę
- Najczęstsze błędy
- Sprawdzone metody nauki

---

## 🎯 Plan nauki

!!! example "Sugerowany harmonogram"
    Dostosuj ten plan do swoich potrzeb i stylu nauki.

### 3-4 tygodnie przed kolokwium
- [ ] Przeczytaj zalecane rozdziały z podręczników
- [ ] Przejrzyj materiały z wykładów
- [ ] Zidentyfikuj trudne tematy

### 2 tygodnie przed
- [ ] Pogłęb trudne tematy
- [ ] Zacznij rozwiązywać pytania z poprzednich lat
- [ ] Stwórz fiszki/notatki

### 1 tydzień przed
- [ ] Intensywne powtórki
- [ ] Rozwiąż wszystkie dostępne pytania
- [ ] Ucz się w grupie (wymiana wiedzy)

### Dzień przed
- [ ] Spokojne powtórki najważniejszych zagadnień
- [ ] **Odpoczynek** - dobry sen jest kluczowy!

---

## 🔗 Przydatne linki

- 📘 [Strona przedmiotu](../../semestr-1/{subject_slug}.md)
- 📚 [Zasoby MedBox](../../zasoby/medbox/semestr-1.md#{subject_slug})
- 📋 [Wszystkie kolokwia - Semestr 1](../semestr-1/index.md)
- 💡 [Strategie nauki](../../egzaminy/strategie.md)
- ❓ [FAQ](../../faq.md)

---

## 📝 Komentarze

!!! tip "Twoja opinia jest ważna"
    Masz dodatkowe informacje o tym kolokwium?
    Znasz dobre źródła do nauki?
    Chcesz ostrzec przed pułapkami?

    [Dodaj komentarz](https://github.com/yourusername/cmuj-wiki/issues/new) lub
    [edytuj tę stronę](https://github.com/yourusername/cmuj-wiki/edit/main/docs/kolokwia/semestr-1/{filename})

---

*Ostatnia aktualizacja: {datetime.now().strftime("%Y-%m-%d")}*

**Powodzenia! 🍀**
"""

    return content, filepath

def main():
    """Main function to generate all kolokwium pages"""

    # Load exam dates data
    print(f"Loading data from {DATA_FILE}...")
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Ensure output directory exists
    KOLOKWIA_DIR.mkdir(parents=True, exist_ok=True)

    pages_generated = 0

    # Process each subject
    for subject_slug, subject_data in data.items():
        if subject_slug == "zasoby_ogolne":
            continue

        subject_name = SUBJECT_NAMES.get(subject_slug, subject_slug.replace("_", " ").title())

        print(f"\nProcessing {subject_name}...")

        # Process kolokwia
        if "kolokwia" in subject_data:
            for idx, kolokwium in enumerate(subject_data["kolokwia"], 1):
                content, filepath = generate_kolokwium_page(
                    subject_slug, subject_name, kolokwium, "kolokwia", idx
                )

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"  ✓ Generated: {filepath.name}")
                pages_generated += 1

        # Process egzaminy
        if "egzaminy" in subject_data:
            for idx, egzamin in enumerate(subject_data["egzaminy"], 1):
                content, filepath = generate_kolokwium_page(
                    subject_slug, subject_name, egzamin, "egzaminy", idx
                )

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"  ✓ Generated: {filepath.name}")
                pages_generated += 1

    print(f"\n{'='*60}")
    print(f"✅ Successfully generated {pages_generated} kolokwium pages!")
    print(f"{'='*60}\n")
    print(f"Output directory: {KOLOKWIA_DIR}")
    print(f"\nNext steps:")
    print(f"1. Review generated pages in {KOLOKWIA_DIR}")
    print(f"2. Update mkdocs.yml navigation to include new pages")
    print(f"3. Run 'mkdocs serve' to preview")

if __name__ == "__main__":
    main()
