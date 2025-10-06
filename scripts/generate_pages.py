#!/usr/bin/env python3
"""
Generate all subject and year index pages for CMUJ Wiki
"""

import os

# Year structure with subjects
YEARS = {
    1: {
        "name": "Rok I",
        "description": "Pierwszy rok - nauki przedkliniczne, podstawy medycyny",
        "subjects": [
            ("anatomia", "Anatomia z embriologią"),
            ("biochemia", "Biochemia z elementami chemii"),
            ("etyka", "Etyka w medycynie"),
            ("fizjologia", "Fizjologia"),
            ("genetyka", "Genetyka z biologią molekularną"),
            ("histologia", "Histologia z cytofizjologią"),
            ("historia-medycyny", "Historia medycyny"),
            ("pierwsza-pomoc", "Pierwsza pomoc"),
            ("wychowanie-fizyczne", "Wychowanie fizyczne"),
            ("bhk", "Szkolenie BHK"),
        ]
    },
    2: {
        "name": "Rok II",
        "description": "Drugi rok - kontynuacja nauk przedklinicznych",
        "subjects": [
            ("biochemia-2", "Biochemia z elementami chemii 2/2"),
            ("biofizyka", "Biofizyka medyczna"),
            ("diagnostyka-lab-1", "Diagnostyka laboratoryjna 1/2"),
            ("farmakologia-1", "Farmakologia 1/2"),
            ("higiena", "Higiena"),
            ("angielski-1", "Język angielski 1/2"),
            ("lnuk-1", "Laboratoryjne nauczanie umiejętności klinicznych 1/4"),
            ("mikrobiologia", "Mikrobiologia z parazytologią i immunologią"),
            ("patomorfologia", "Patologia – Patomorfologia"),
            ("patofizjologia", "Patologia – Patofizjologia"),
            ("pierwsza-pomoc-2", "Pierwsza pomoc 2/2"),
            ("psychologia-1", "Psychologia lekarska 1/2"),
            ("socjologia", "Socjologia medycyny"),
            ("telemedycyna", "Telemedycyna z elementami symulacji medycznej"),
            ("wstep-klinika", "Wstęp do nauk klinicznych"),
        ]
    },
    3: {
        "name": "Rok III",
        "description": "Trzeci rok - wprowadzenie do nauk klinicznych",
        "subjects": [
            ("chirurgia-1", "Chirurgia 1/4"),
            ("choroby-wewnetrzne-1", "Choroby wewnętrzne 1/4"),
            ("dermatologia", "Dermatologia i wenerologia"),
            ("diagnostyka-lab-2", "Diagnostyka laboratoryjna 2/2"),
            ("epidemiologia", "Epidemiologia i zdrowie publiczne"),
            ("farmakologia-2", "Farmakologia 2/2"),
            ("ginekologia-1", "Ginekologia i położnictwo 1/4"),
            ("angielski-2", "Język angielski 2/3"),
            ("lnuk-2", "Laboratoryjne nauczanie umiejętności klinicznych 2/4"),
            ("pediatria-1", "Pediatria 1/4"),
            ("psychologia-2", "Psychologia lekarska 2/2"),
            ("radiologia", "Radiologia"),
        ]
    },
    4: {
        "name": "Rok IV",
        "description": "Czwarty rok - rotacje kliniczne i specjalizacje",
        "subjects": [
            ("anestezjologia", "Anestezjologia i intensywna terapia"),
            ("chirurgia", "Chirurgia"),
            ("kardiochirurgia", "Kardiochirurgia i chirurgia naczyniowa"),
            ("chirurgia-szczekowa", "Chirurgia szczękowo-twarzowa"),
            ("chirurgia-dziecieca", "Chirurgia dziecięca"),
            ("choroby-wewnetrzne", "Choroby wewnętrzne"),
            ("genetyka-kliniczna", "Genetyka kliniczna"),
            ("ginekologia", "Ginekologia i położnictwo"),
            ("immunologia", "Immunologia kliniczna"),
            ("laryngologia", "Laryngologia"),
            ("medycyna-nuklearna", "Medycyna nuklearna"),
            ("medycyna-pracy", "Medycyna pracy"),
            ("medycyna-rodzinna", "Medycyna rodzinna"),
            ("neurologia", "Neurologia"),
            ("okulistyka", "Okulistyka"),
            ("pediatria", "Pediatria"),
            ("usg", "Podstawy ultrasonografii"),
            ("prawo-medyczne", "Prawo medyczne i deontologia lekarska"),
            ("stomatologia", "Propedeutyka stomatologii"),
            ("psychiatria", "Psychiatria"),
        ]
    },
    5: {
        "name": "Rok V",
        "description": "Piąty rok - zaawansowane nauki kliniczne",
        "subjects": [
            ("anestezjologia", "Anestezjologia i intensywna terapia"),
            ("chirurgia", "Chirurgia"),
            ("choroby-wewnetrzne", "Choroby wewnętrzne"),
            ("choroby-zakażne", "Choroby zakaźne"),
            ("geriatria", "Geriatria i medycyna paliatywna"),
            ("ginekologia", "Ginekologia i położnictwo"),
            ("medycyna-ratunkowa", "Medycyna ratunkowa"),
            ("medycyna-sadowa", "Medycyna sądowa"),
            ("onkologia", "Onkologia i hematologia"),
            ("ortopedia", "Ortopedia i traumatologia"),
            ("pediatria", "Pediatria"),
            ("psychiatria", "Psychiatria"),
            ("psychoterapia", "Psychoterapia"),
            ("rehabilitacja", "Rehabilitacja"),
        ]
    },
    6: {
        "name": "Rok VI",
        "description": "Szósty rok - praktyki końcowe i przygotowanie do LEK",
        "subjects": [
            ("choroby-wewnetrzne", "Choroby wewnętrzne"),
            ("chirurgia", "Chirurgia"),
            ("pediatria", "Pediatria"),
            ("ginekologia", "Ginekologia i położnictwo"),
            ("psychiatria", "Psychiatria"),
            ("medycyna-ratunkowa", "Medycyna ratunkowa"),
            ("medycyna-rodzinna", "Medycyna rodzinna"),
            ("repetytorium", "Repetytorium nauk klinicznych"),
        ]
    }
}

SUBJECT_TEMPLATE = """# {subject_name}

## 📋 Informacje ogólne

- **Prowadzący**: [Lista prowadzących](../prowadzacy/index.md)
- **ECTS**: (do uzupełnienia)
- **Rok/Semestr**: {year_name}, Semestr (do uzupełnienia)

## 📚 Materiały

### Literatura

!!! note "Polecane podręczniki"
    (Do uzupełnienia - dodaj polecane książki i skrypty)

### Wykłady

#### 2024/2025
(Do uzupełnienia - dodaj linki do wykładów)

#### Archiwum
- [Materiały z poprzednich lat](https://drive.google.com/drive/folders/1SpFEsQDlYYFfqb4o5AEM0aGhNiRsWlTN)

### Ćwiczenia/Seminaria

(Do uzupełnienia - dodaj materiały do ćwiczeń)

### Egzaminy

#### Pytania egzaminacyjne
(Do uzupełnienia - dodaj pytania z ubiegłych lat)

### Kolokwia

(Do uzupełnienia - dodaj materiały do kolokwiów)

## 💬 Komentarze studentów

!!! tip "Wskazówki"
    (Do uzupełnienia - podziel się wskazówkami dla młodszych roczników)

## 🔗 Przydatne linki

- [Oficjalny sylabus UJ CM](https://sylabus.cm-uj.krakow.pl/pl/7/1/7/1/1)
- [Strona wydziału](https://wl.cm.uj.edu.pl/)

---

*Pomóż rozwijać tę stronę! Kliknij ikonę ✏️ w prawym górnym rogu, aby dodać materiały.*
"""

YEAR_INDEX_TEMPLATE = """# {year_name}

{description}

## 📚 Przedmioty w tym roku

{subjects_list}

## 💡 Wskazówki dla tego roku

!!! tip "Ogólne wskazówki"
    (Do uzupełnienia - dodaj ogólne rady dla studentów tego roku)

## 🔗 Przydatne informacje

- [Harmonogramy zajęć](https://wl.cm.uj.edu.pl/dydaktyka/kierunek-lekarski/)
- [Sylabus oficjalny](https://sylabus.cm-uj.krakow.pl/pl/7/1/7/1/1)
- [Materiały Google Drive](https://drive.google.com/drive/folders/1SpFEsQDlYYFfqb4o5AEM0aGhNiRsWlTN)

---

*Wybierz przedmiot z listy powyżej lub użyj wyszukiwarki.*
"""


def create_subject_page(year_num, filename, subject_name, year_name):
    """Create a subject page"""
    content = SUBJECT_TEMPLATE.format(
        subject_name=subject_name,
        year_name=year_name
    )
    path = f"docs/rok-{year_num}/{filename}.md"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {path}")


def create_year_index(year_num, year_data):
    """Create year index page"""
    subjects_list = "\n".join([
        f"- [{subject_name}]({filename}.md)"
        for filename, subject_name in year_data["subjects"]
    ])

    content = YEAR_INDEX_TEMPLATE.format(
        year_name=year_data["name"],
        description=year_data["description"],
        subjects_list=subjects_list
    )

    path = f"docs/rok-{year_num}/index.md"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {path}")


def main():
    """Generate all pages"""
    print("🚀 Generating CMUJ Wiki pages...\n")

    for year_num, year_data in YEARS.items():
        print(f"\n📖 Generating {year_data['name']}...")

        # Create year index
        create_year_index(year_num, year_data)

        # Create all subject pages for this year
        for filename, subject_name in year_data["subjects"]:
            create_subject_page(year_num, filename, subject_name, year_data["name"])

    print("\n✨ All pages generated successfully!")
    print(f"\n📊 Statistics:")
    total_subjects = sum(len(year_data["subjects"]) for year_data in YEARS.values())
    print(f"   - {len(YEARS)} years")
    print(f"   - {total_subjects} subject pages")
    print(f"   - {len(YEARS)} year index pages")


if __name__ == "__main__":
    main()
