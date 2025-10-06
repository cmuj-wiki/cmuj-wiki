#!/usr/bin/env python3
"""
Reorganize wiki from year-based (rok-X) to semester-based (semestr-X) structure.
Based on typical Polish medical curriculum: 6 years = 12 semesters
"""

import os
import shutil

# Mapping of subjects from current structure to semesters
# Based on homepage tables and typical medical curriculum
SEMESTER_STRUCTURE = {
    1: [  # Semestr 1 (Rok 1, Semestr zimowy)
        ("anatomia", "Anatomia z embriologią"),
        ("biochemia", "Biochemia z elementami chemii"),
        ("histologia", "Histologia z cytofizjologią"),
        ("etyka", "Etyka w medycynie"),
        ("historia-medycyny", "Historia medycyny"),
        ("wychowanie-fizyczne", "Wychowanie fizyczne"),
        ("bhk", "Szkolenie BHK"),
    ],
    2: [  # Semestr 2 (Rok 1, Semestr letni)
        ("anatomia", "Anatomia z embriologią"),
        ("biochemia", "Biochemia z elementami chemii"),
        ("fizjologia", "Fizjologia"),
        ("genetyka", "Genetyka z biologią molekularną"),
        ("histologia", "Histologia z cytofizjologią"),
        ("pierwsza-pomoc", "Pierwsza pomoc"),
    ],
    3: [  # Semestr 3 (Rok 2, Semestr zimowy)
        ("biochemia-2", "Biochemia 2/2"),
        ("biofizyka", "Biofizyka medyczna"),
        ("farmakologia-1", "Farmakologia 1/2"),
        ("mikrobiologia", "Mikrobiologia"),
        ("patomorfologia", "Patologia – Patomorfologia"),
        ("patofizjologia", "Patologia – Patofizjologia"),
        ("psychologia-1", "Psychologia lekarska 1/2"),
    ],
    4: [  # Semestr 4 (Rok 2, Semestr letni)
        ("diagnostyka-lab-1", "Diagnostyka laboratoryjna 1/2"),
        ("higiena", "Higiena"),
        ("angielski-1", "Język angielski 1/2"),
        ("lnuk-1", "LNUK 1/4"),
        ("pierwsza-pomoc-2", "Pierwsza pomoc 2/2"),
        ("socjologia", "Socjologia medycyny"),
        ("telemedycyna", "Telemedycyna"),
        ("wstep-klinika", "Wstęp do nauk klinicznych"),
    ],
    5: [  # Semestr 5 (Rok 3, Semestr zimowy)
        ("chirurgia-1", "Chirurgia 1/4"),
        ("choroby-wewnetrzne-1", "Choroby wewnętrzne 1/4"),
        ("diagnostyka-lab-2", "Diagnostyka laboratoryjna 2/2"),
        ("farmakologia-2", "Farmakologia 2/2"),
        ("lnuk-2", "LNUK 2/4"),
        ("pediatria-1", "Pediatria 1/4"),
        ("psychologia-2", "Psychologia lekarska 2/2"),
    ],
    6: [  # Semestr 6 (Rok 3, Semestr letni)
        ("dermatologia", "Dermatologia i wenerologia"),
        ("epidemiologia", "Epidemiologia i zdrowie publiczne"),
        ("ginekologia-1", "Ginekologia i położnictwo 1/4"),
        ("angielski-2", "Język angielski 2/3"),
        ("radiologia", "Radiologia"),
    ],
    7: [  # Semestr 7 (Rok 4, Semestr zimowy)
        ("anestezjologia", "Anestezjologia i intensywna terapia"),
        ("chirurgia", "Chirurgia"),
        ("choroby-wewnetrzne", "Choroby wewnętrzne"),
        ("genetyka-kliniczna", "Genetyka kliniczna"),
        ("ginekologia", "Ginekologia i położnictwo"),
        ("laryngologia", "Laryngologia"),
        ("neurologia", "Neurologia"),
        ("pediatria", "Pediatria"),
    ],
    8: [  # Semestr 8 (Rok 4, Semestr letni)
        ("kardiochirurgia", "Kardiochirurgia"),
        ("chirurgia-szczekowa", "Chirurgia szczękowo-twarzowa"),
        ("chirurgia-dziecieca", "Chirurgia dziecięca"),
        ("immunologia", "Immunologia kliniczna"),
        ("medycyna-nuklearna", "Medycyna nuklearna"),
        ("medycyna-pracy", "Medycyna pracy"),
        ("medycyna-rodzinna", "Medycyna rodzinna"),
        ("okulistyka", "Okulistyka"),
        ("usg", "Podstawy ultrasonografii"),
        ("prawo-medyczne", "Prawo medyczne"),
        ("stomatologia", "Propedeutyka stomatologii"),
        ("psychiatria", "Psychiatria"),
    ],
    9: [  # Semestr 9 (Rok 5, Semestr zimowy)
        ("anestezjologia", "Anestezjologia"),
        ("chirurgia", "Chirurgia"),
        ("choroby-wewnetrzne", "Choroby wewnętrzne"),
        ("choroby-zakażne", "Choroby zakaźne"),
        ("medycyna-ratunkowa", "Medycyna ratunkowa"),
        ("onkologia", "Onkologia i hematologia"),
        ("pediatria", "Pediatria"),
        ("psychiatria", "Psychiatria"),
    ],
    10: [  # Semestr 10 (Rok 5, Semestr letni)
        ("geriatria", "Geriatria i medycyna paliatywna"),
        ("ginekologia", "Ginekologia i położnictwo"),
        ("medycyna-sadowa", "Medycyna sądowa"),
        ("ortopedia", "Ortopedia i traumatologia"),
        ("psychoterapia", "Psychoterapia"),
        ("rehabilitacja", "Rehabilitacja"),
    ],
    11: [  # Semestr 11 (Rok 6, Semestr zimowy)
        ("choroby-wewnetrzne", "Choroby wewnętrzne"),
        ("chirurgia", "Chirurgia"),
        ("pediatria", "Pediatria"),
        ("ginekologia", "Ginekologia i położnictwo"),
        ("medycyna-ratunkowa", "Medycyna ratunkowa"),
    ],
    12: [  # Semestr 12 (Rok 6, Semestr letni)
        ("psychiatria", "Psychiatria"),
        ("medycyna-rodzinna", "Medycyna rodzinna"),
        ("repetytorium", "Repetytorium"),
    ],
}

def create_semester_structure():
    """Create new semester-based folder structure and copy files."""

    base_dir = "docs"

    # Create semester directories
    for sem_num in range(1, 13):
        sem_dir = os.path.join(base_dir, f"semestr-{sem_num}")
        os.makedirs(sem_dir, exist_ok=True)
        print(f"Created {sem_dir}")

        # Create index page for this semester
        subjects = SEMESTER_STRUCTURE.get(sem_num, [])

        # Determine which year this semester belongs to
        year = ((sem_num - 1) // 2) + 1
        season = "zimowy" if sem_num % 2 == 1 else "letni"

        index_content = f"""# Semestr {sem_num}

**Rok {year} • Semestr {season}**

## 📚 Przedmioty w tym semestrze

"""
        for slug, name in subjects:
            index_content += f"- [{name}]({slug}.md)\n"

        index_content += f"""
## 💡 Wskazówki dla tego semestru

!!! tip "Ogólne wskazówki"
    (Do uzupełnienia - dodaj ogólne rady dla studentów tego semestru)

## 🔗 Przydatne informacje

- [Harmonogramy zajęć](https://wl.cm.uj.edu.pl/dydaktyka/kierunek-lekarski/)
- [Sylabus oficjalny](https://sylabus.cm-uj.krakow.pl/pl/8/1/7/1/1#nav-tab-{sem_num + 6})
- [Materiały Google Drive](https://drive.google.com/drive/folders/1SpFEsQDlYYFfqb4o5AEM0aGhNiRsWlTN)

---

*Wybierz przedmiot z listy powyżej lub użyj wyszukiwarki.*
"""

        with open(os.path.join(sem_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write(index_content)

        print(f"  Created index for Semestr {sem_num}")

        # Copy or create subject files
        for slug, name in subjects:
            # Try to find existing file in rok-X directories
            source_file = None
            for year_num in range(1, 7):
                potential_path = os.path.join(base_dir, f"rok-{year_num}", f"{slug}.md")
                if os.path.exists(potential_path):
                    source_file = potential_path
                    break

            dest_file = os.path.join(sem_dir, f"{slug}.md")

            if source_file and not os.path.exists(dest_file):
                # Copy existing file
                shutil.copy2(source_file, dest_file)
                print(f"  Copied {slug}.md")
            elif not os.path.exists(dest_file):
                # Create template file
                template = f"""# {name}

## 📖 Opis przedmiotu

> **Do uzupełnienia**: Krótki opis przedmiotu, zakres materiału

## 📚 Materiały do nauki

### Wykłady
- [Link do materiałów](https://drive.google.com/...)

### Ćwiczenia/Seminaria
- [Link do materiałów](https://drive.google.com/...)

### Polecane podręczniki
- **Do uzupełnienia**: Lista polecanych książek

## 📝 Egzaminy i kolokwia

### Format egzaminu
- **Do uzupełnienia**: Jak wygląda egzamin (test/ustny/praktyczny)

### Materiały egzaminacyjne
- [Pytania z poprzednich lat](link)
- [Przykładowe testy](link)

## 👨‍⚕️ Prowadzący

> **Do uzupełnienia**: Informacje o prowadzących, ich wymagania, styl nauczania

## 💬 Komentarze studentów

!!! quote "Wskazówki od starszych roczników"
    **Do uzupełnienia**: Rady, jak się przygotować, na co zwrócić uwagę

## 🔗 Przydatne linki

- [Sylabus oficjalny](https://sylabus.cm-uj.krakow.pl/)
- [Materiały na Google Drive](https://drive.google.com/drive/folders/1SpFEsQDlYYFfqb4o5AEM0aGhNiRsWlTN)

---

*Jeśli masz materiały lub wskazówki do dodania, [zobacz jak edytować wiki](../jak-edytowac.md)*
"""
                with open(dest_file, "w", encoding="utf-8") as f:
                    f.write(template)
                print(f"  Created template for {slug}.md")

if __name__ == "__main__":
    print("Creating semester-based structure...\n")
    create_semester_structure()
    print("\n✅ Semester structure created successfully!")
