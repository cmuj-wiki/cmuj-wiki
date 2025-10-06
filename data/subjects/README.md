# Subject Data System

This directory contains YAML data files that serve as the **single source of truth** for official subject information and MedBox resources across the CMUJ Wiki.

## 📁 Current Status

### ✅ Semester 1 - Complete (7/7)

All Semester 1 subjects have YAML files and updated pages:

1. **anatomia.yml** → [anatomia.md](../../docs/semestr-1/anatomia.md) ✅
2. **biochemia.yml** → [biochemia.md](../../docs/semestr-1/biochemia.md) ✅
3. **histologia.yml** → [histologia.md](../../docs/semestr-1/histologia.md) ✅
4. **bhk.yml** → [bhk.md](../../docs/semestr-1/bhk.md) ✅
5. **etyka.yml** → [etyka.md](../../docs/semestr-1/etyka.md) ✅
6. **historia-medycyny.yml** → [historia-medycyny.md](../../docs/semestr-1/historia-medycyny.md) ✅
7. **wychowanie-fizyczne.yml** → [wychowanie-fizyczne.md](../../docs/semestr-1/wychowanie-fizyczne.md) ✅

### ⏳ Remaining Work

- **Fill in MedBox Google Drive folder IDs** - Replace all `[FOLDER_ID]` placeholders
- **Verify ECTS and hours data** - Some fields marked with `TODO:` need verification
- **Add syllabus PDF UUIDs** - Extract from actual syllabus URLs
- **Create YAML files for Semesters 2-12** (72 remaining subjects)

## 🔧 How It Works

### Architecture

```
data/subjects/
├── subject.yml (YAML data - SOURCE OF TRUTH)
    ↓
scripts/update_subject_pages.py (Smart updater)
    ↓
docs/semestr-X/subject.md (Generated + Manual content)
```

### Key Features

1. **Marker-Based Replacement** - Auto-generated sections wrapped in HTML comments:
   - `<!-- START: AUTO-GENERATED-OFFICIAL -->` ... `<!-- END: AUTO-GENERATED-OFFICIAL -->`
   - `<!-- START: AUTO-GENERATED-MEDBOX -->` ... `<!-- END: AUTO-GENERATED-MEDBOX -->`

2. **Content Preservation** - All manual student content outside markers is preserved

3. **Single Source of Truth** - Edit YAML → Run script → Pages update automatically

## 📝 YAML File Structure

```yaml
slug: anatomia
name: "Anatomia z embriologią"
semester: 1
last_verified: "2025-10-05"

syllabus:
  ects: 14
  coordinator:
    name: "Katedra Anatomii"
    email: "anatomia@cm-uj.krakow.pl"
  hours:
    total: 94
    wyklady: 20
    cwiczenia: 74
  exam_type: "Egzamin praktyczny i teoretyczny"
  syllabus_pdf: "https://sylabus.cm-uj.krakow.pl/pl/document/UUID.pdf"
  department_url: "http://anatomia.cm-uj.krakow.pl/"

medbox:
  folder_main: "https://drive.google.com/drive/folders/FOLDER_ID"
  resources:
    ksiazki:
      - title: "Bochenek - Anatomia Człowieka"
        url: "https://drive.google.com/drive/folders/FOLDER_ID"
        description: "Klasyczny polski podręcznik anatomii"

kolokwia:
  - title: "Kolokwium 1 - Osteologia i czaszka"
    date: "2025-11-06"
    link: "kolokwia/semestr-1/anatomia-kolokwia-1"
```

## 🚀 Usage

### Update Single Subject

```bash
python3 scripts/update_subject_pages.py --subject anatomia
```

### Update All Subjects

```bash
python3 scripts/update_subject_pages.py --all
```

## 📦 MedBox Resource Categories

The system supports these MedBox resource categories:

- `ksiazki` → 📖 Podręczniki i książki
- `szpilki` → 📌 Preparaty (egzamin praktyczny)
- `prezentacje` → 📊 Prezentacje z wykładów
- `skrypty` → 📝 Skrypty i notatki
- `embriologia` → 🧬 Embriologia
- `bazy` → 💾 Bazy danych
- `wyklady` → 🎓 Wykłady
- `kolokwia` → 📝 Pytania z kolokwiów
- `cwiczenia` → ⚗️ Materiały do ćwiczeń
- `preparaty` → 🔬 Preparaty mikroskopowe
- `atlasy` → 🗺️ Atlasy

## 🔍 Finding MedBox Folder IDs

To fill in `[FOLDER_ID]` placeholders:

1. Open the Google Drive folder in your browser
2. Copy the URL: `https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWxYz`
3. Extract the ID: `1AbCdEfGhIjKlMnOpQrStUvWxYz`
4. Replace `[FOLDER_ID]` in the YAML file

## 📅 Finding Official Data

### ECTS, Hours, Coordinator

Search for: `[subject name] uj cm lekarski harmonogram`

Examples:
- Anatomia: http://anatomia.cm-uj.krakow.pl/dydaktyka/kierunek-lekarski/
- Biochemia: http://biochemia.cm-uj.krakow.pl/dydaktyka/
- Histologia: http://histologia.cm-uj.krakow.pl/dydaktyka/kierunek-lekarski/

### Syllabus PDFs

1. Go to: https://sylabus.cm-uj.krakow.pl/
2. Navigate to subject page
3. Copy PDF URL with UUID

## 🎯 Next Steps

### Immediate (User Action Required)

1. **Fill in MedBox folder IDs**
   - Open `data/subjects/*.yml` files
   - Replace all `[FOLDER_ID]` with actual Google Drive IDs
   - Replace `[ANATOMIA_MAIN_FOLDER_ID]`, `[BIOCHEMIA_FOLDER_ID]`, etc.

2. **Verify placeholder data**
   - Check `TODO:` comments in YAML files
   - Verify ECTS values match official syllabi
   - Update coordinator emails if needed

3. **Run updater to apply changes**
   ```bash
   python3 scripts/update_subject_pages.py --all
   ```

### Future Expansion

1. **Create YAMLs for Semester 2**
   - Analyze subjects in `docs/semestr-2/`
   - Create corresponding YAML files
   - Run updater

2. **Repeat for Semesters 3-12**
   - Total: 72 remaining subjects across 11 semesters

3. **Yearly Maintenance**
   - Update `last_verified` dates
   - Check for syllabus changes
   - Update kolokwium dates

## 📄 Generated Output Example

When a page is updated, it gets two auto-generated sections:

### Official Information Section

```markdown
<!-- START: AUTO-GENERATED-OFFICIAL -->
## 📋 Informacje o przedmiocie

| | |
|---|---|
| **ECTS** | 14 |
| **Koordynator** | Katedra Anatomii ([anatomia@cm-uj.krakow.pl](mailto:anatomia@cm-uj.krakow.pl)) |
| **Godziny** | Wykłady: 20h, Ćwiczenia: 74h |
| **Forma zaliczenia** | Egzamin praktyczny i teoretyczny |

### 🎯 Kolokwia i egzaminy
- [Kolokwium 1 - Osteologia i czaszka](kolokwia/semestr-1/anatomia-kolokwia-1) - 2025-11-06
<!-- END: AUTO-GENERATED-OFFICIAL -->
```

### MedBox Resources Section

```markdown
<!-- START: AUTO-GENERATED-MEDBOX -->
## 📚 Zasoby MedBox

### 📖 Podręczniki i książki
- **[Bochenek - Anatomia Człowieka](https://drive.google.com/drive/folders/ID)**
  <br>*Klasyczny polski podręcznik anatomii*
<!-- END: AUTO-GENERATED-MEDBOX -->
```

## 🛡️ Safety Features

- **Never overwrites manual content** - Only replaces marked sections
- **Preserves student contributions** - Comments, tips, and manual materials remain intact
- **Version controlled** - All changes tracked in Git
- **Timestamped** - Each update includes generation timestamp

## 🔗 Related Files

- [`scripts/update_subject_pages.py`](../../scripts/update_subject_pages.py) - The updater script
- [`docs/zasoby/medbox-info.md`](../../docs/zasoby/medbox-info.md) - MedBox information page
- [`data/exam_dates_manual.yml`](../exam_dates_manual.yml) - Exam dates data

---

**Last Updated:** 2025-10-05
**System Version:** 1.0
**Maintained by:** CMUJ Wiki Contributors
