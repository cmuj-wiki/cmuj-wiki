#!/usr/bin/env python3
"""
Scrape UJ Collegium Medicum Syllabus Data

Scrapes official syllabus HTML pages to extract:
- Subject names
- ECTS points
- Hours (wykłady/ćwiczenia/seminaria)
- Exam format
- Semester assignment

Outputs: data/syllabus_scraped.json
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path

# Syllabus URLs for each semester
SYLLABUS_URLS = {
    1: "https://sylabus.cm-uj.krakow.pl/pl/8/1/7/1/1",  # Semestr 1
    # TODO: Add remaining semesters 2-12
}

def slugify(text):
    """Convert Polish text to URL-friendly slug"""
    text = text.lower()
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l',
        'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        ' z ': '-', ' i ': '-', ' ': '-', '/': '-',
        ',': '', '.': '', '(': '', ')': ''
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Remove multiple dashes
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def parse_hours(hours_text):
    """
    Parse hours like '60 (w tym: 30 w., 30 ćw.)'
    Returns: {total: 60, wyklady: 30, cwiczenia: 30, seminaria: 0}
    """
    result = {
        'total': 0,
        'wyklady': 0,
        'cwiczenia': 0,
        'seminaria': 0,
        'e_learning': 0
    }

    if not hours_text:
        return result

    # Extract total hours
    total_match = re.search(r'(\d+)', hours_text)
    if total_match:
        result['total'] = int(total_match.group(1))

    # Extract detailed breakdown
    if 'w.' in hours_text:
        wyk_match = re.search(r'(\d+)\s*w\.', hours_text)
        if wyk_match:
            result['wyklady'] = int(wyk_match.group(1))

    if 'ćw.' in hours_text:
        cw_match = re.search(r'(\d+)\s*ćw\.', hours_text)
        if cw_match:
            result['cwiczenia'] = int(cw_match.group(1))

    if 'sem.' in hours_text:
        sem_match = re.search(r'(\d+)\s*sem\.', hours_text)
        if sem_match:
            result['seminaria'] = int(sem_match.group(1))

    if 'e-learning' in hours_text.lower():
        el_match = re.search(r'(\d+)\s*e-learning', hours_text, re.IGNORECASE)
        if el_match:
            result['e_learning'] = int(el_match.group(1))

    return result

def scrape_semester(url, semester_num):
    """Scrape a single semester page"""
    print(f"\nScraping Semester {semester_num}: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    subjects = []

    # Find all subject tables (they have specific structure)
    # The syllabus uses tables with subject information
    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')

            if len(cells) < 4:
                continue

            # Extract data from cells
            # Typical structure: [Subject Name, Hours, ECTS, Verification, Obligatory]
            subject_name = cells[0].get_text(strip=True)
            hours_text = cells[1].get_text(strip=True) if len(cells) > 1 else ""
            ects_text = cells[2].get_text(strip=True) if len(cells) > 2 else ""
            verification_text = cells[3].get_text(strip=True) if len(cells) > 3 else ""

            # Skip header rows and empty cells
            if not subject_name or subject_name.lower() in ['nazwa', 'przedmiot', 'lp.']:
                continue

            # Parse ECTS
            ects = 0
            ects_match = re.search(r'(\d+)', ects_text)
            if ects_match:
                ects = int(ects_match.group(1))

            # Parse hours
            hours = parse_hours(hours_text)

            # Determine exam type
            exam_type = "Nieznany"
            if 'egzamin' in verification_text.lower():
                exam_type = "Egzamin"
            elif 'zaliczenie' in verification_text.lower():
                exam_type = "Zaliczenie"

            # Create subject entry
            subject = {
                'name': subject_name,
                'slug': slugify(subject_name),
                'semester': semester_num,
                'ects': ects,
                'hours': hours,
                'exam_type': exam_type,
                'verification': verification_text,
                'source_url': url
            }

            subjects.append(subject)
            print(f"  ✓ {subject_name} (ECTS: {ects}, Hours: {hours['total']})")

    return subjects

def main():
    """Main scraping function"""
    print("="*60)
    print("UJ CM Syllabus Scraper")
    print("="*60)

    all_subjects = []

    for semester, url in SYLLABUS_URLS.items():
        subjects = scrape_semester(url, semester)
        all_subjects.extend(subjects)

    # Save to JSON
    output_file = Path(__file__).parent.parent / "data" / "syllabus_scraped.json"
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_subjects, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ Scraped {len(all_subjects)} subjects")
    print(f"📁 Saved to: {output_file}")
    print(f"{'='*60}")

    # Summary by semester
    by_semester = {}
    for subj in all_subjects:
        sem = subj['semester']
        by_semester[sem] = by_semester.get(sem, 0) + 1

    print(f"\nSummary by semester:")
    for sem in sorted(by_semester.keys()):
        print(f"  Semestr {sem}: {by_semester[sem]} subjects")

if __name__ == "__main__":
    main()
