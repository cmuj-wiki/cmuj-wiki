#!/usr/bin/env python3
"""
ULEPSZONA wersja generatora ICS.
Uwzględnia:
1. Precyzyjne zakresy dat z komórek (np. "24.XI-19.I")
2. Lokalizacje/adresy
3. Dni wolne (nie generuje wydarzeń w święta)
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import re
from icalendar import Calendar, Event
from zoneinfo import ZoneInfo

WARSAW_TZ = ZoneInfo("Europe/Warsaw")

# Semestr zimowy 2024/2025 - TYLKO ZAJĘCIA (bez sesji!)
SEMESTER_START = datetime(2024, 10, 1, tzinfo=WARSAW_TZ)   # Początek zajęć
SEMESTER_END = datetime(2025, 1, 31, tzinfo=WARSAW_TZ)     # Koniec zajęć (przed sesją 1-28.II)

MONTHS = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6,
    'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12
}

def parse_date_range(date_str):
    """Parsuje zakresy dat z rzymskimi miesiącami."""
    if not date_str:
        return None

    # NOWE: Format "do DD.MM" - od początku semestru do podanej daty
    if date_str.startswith('do '):
        end_pattern = r'do\s+(\d{1,2})\.([IVX]+)'
        match = re.search(end_pattern, date_str)
        if match:
            day, month = match.groups()
            year = 2024 if MONTHS[month] >= 10 else 2025
            end = datetime(year, MONTHS[month], int(day), tzinfo=WARSAW_TZ)
            # Start to początek semestru
            return (SEMESTER_START, end)

    # Zakres: "24.XI-19.I" lub "24.XI - 19.I"
    range_pattern = r'(\d{1,2})\.([IVX]+)(?:\.\d{4})?\s*-\s*(\d{1,2})\.([IVX]+)(?:\.\d{4})?'
    match = re.search(range_pattern, date_str)

    if match:
        day1, month1, day2, month2 = match.groups()

        year1 = 2024 if MONTHS[month1] >= 10 else 2025
        year2 = year1 if MONTHS[month2] >= MONTHS[month1] else year1 + 1

        start = datetime(year1, MONTHS[month1], int(day1), tzinfo=WARSAW_TZ)
        end = datetime(year2, MONTHS[month2], int(day2), tzinfo=WARSAW_TZ)
        return (start, end)

    # Pojedyncza data: "3.X.2025" lub "3.X"
    single_pattern = r'(\d{1,2})\.([IVX]+)(?:\.(\d{4}))?'
    match = re.search(single_pattern, date_str)

    if match:
        day, month, year = match.groups()
        year = int(year) if year else (2024 if MONTHS[month] >= 10 else 2025)
        date = datetime(year, MONTHS[month], int(day), tzinfo=WARSAW_TZ)
        return (date, date)

    return None

def get_class_dates(cls, semester_start, semester_end, holidays):
    """
    Zwraca listę dat kiedy odbywa się dane zajęcie.
    Uwzględnia zakresy dat z komórki i pomija święta.
    """

    # Jeśli są określone daty w komórce, użyj ich
    if cls.get('dates') and len(cls['dates']) > 0:
        date_range = parse_date_range(cls['dates'][0])
        if date_range:
            start, end = date_range
        else:
            start, end = semester_start, semester_end
    else:
        start, end = semester_start, semester_end

    dates = []
    current = start

    # Przejdź do pierwszego wystąpienia tego dnia tygodnia
    while current.weekday() != cls['day']:
        current += timedelta(days=1)

    # Generuj daty co tydzień, pomijając święta
    while current <= end:
        # Sprawdź czy to nie jest dzień wolny
        is_holiday = False
        for holiday in holidays:
            if current.date() == holiday.date():
                is_holiday = True
                break

        if not is_holiday:
            dates.append(current)

        current += timedelta(weeks=1)

    return dates

def generate_ics_for_group(group_num, classes, holidays, output_path):
    """Generuje plik ICS dla danej grupy."""

    group_classes = [c for c in classes if c['group'] == group_num]

    if not group_classes:
        print(f"⚠️  Brak zajęć dla grupy {group_num}")
        return

    cal = Calendar()
    cal.add('prodid', '-//CMUJ Wiki//Plan Zajęć//PL')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', f'Plan Zajęć - Grupa {group_num}')
    cal.add('x-wr-timezone', 'Europe/Warsaw')
    cal.add('x-wr-caldesc', f'Plan zajęć dla grupy {group_num} - I rok Kierunku Lekarskiego UJ CM (z adresami i dniami wolnymi)')

    event_count = 0

    for cls in group_classes:
        dates = get_class_dates(cls, SEMESTER_START, SEMESTER_END, holidays)

        for date in dates:
            event = Event()

            # Tytuł wydarzenia
            subject = cls['subject']
            if cls.get('type'):
                subject = f"{subject} ({cls['type']})"

            event.add('summary', subject)

            # Czas
            start_time = date.replace(
                hour=cls['hour'] or 8,
                minute=cls['minute'] or 0,
                second=0,
                microsecond=0
            )

            # Użyj rzeczywistego czasu trwania z danych (wykrytego z scalonych komórek)
            duration_minutes = cls.get('duration', 90)  # domyślnie 90 min
            duration = timedelta(minutes=duration_minutes)
            end_time = start_time + duration

            event.add('dtstart', start_time)
            event.add('dtend', end_time)

            # Lokalizacja - TERAZ Z ADRESEM!
            if cls.get('location'):
                event.add('location', cls['location'])

            # Opis
            description_parts = []
            if cls.get('type'):
                description_parts.append(f"Typ: {cls['type']}")
            if cls.get('location'):
                description_parts.append(f"Miejsce: {cls['location']}")
            if cls.get('dates'):
                description_parts.append(f"Okres: {cls['dates'][0]}")
            if cls.get('time'):
                description_parts.append(f"Godziny: {cls['time']}")

            description_parts.append(f"\nGrupa: {group_num}")
            description_parts.append(f"\n🩺 Wygenerowano przez CMUJ Wiki")
            description_parts.append("📍 Adresy z oficjalnego planu UJ CM")

            event.add('description', '\n'.join(description_parts))

            # UID
            event.add('uid', f"{group_num}-{cls['subject']}-{start_time.isoformat()}@cmuj-wiki")
            event.add('dtstamp', datetime.now(tz=WARSAW_TZ))

            # Kategorie
            if cls.get('type'):
                if 'wykład' in cls.get('type', '').lower():
                    event.add('categories', ['WYKŁAD'])
                elif 'ćw' in cls.get('type', '').lower():
                    event.add('categories', ['ĆWICZENIA'])
                elif 'sem' in cls.get('type', '').lower():
                    event.add('categories', ['SEMINARIUM'])

            cal.add_component(event)
            event_count += 1

    # Zapisz
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(cal.to_ical())

    print(f"✅ Grupa {group_num}: {len(group_classes)} zajęć → {event_count} wydarzeń (pominieto {len(holidays)} świąt) → {output_path.name}")

if __name__ == "__main__":
    # Wczytaj dane
    with open('docs/static/schedule_data_v2.json', 'r', encoding='utf-8') as f:
        classes = json.load(f)

    # Wczytaj dni wolne
    with open('docs/static/holidays.json', 'r', encoding='utf-8') as f:
        holidays_data = json.load(f)
        # New format: [{date, type, name}, ...] - extract dates only
        if holidays_data and isinstance(holidays_data[0], dict):
            holidays = [datetime.fromisoformat(h['date']).replace(tzinfo=WARSAW_TZ) for h in holidays_data]
        else:
            # Old format: ["YYYY-MM-DD", ...]
            holidays = [datetime.fromisoformat(h).replace(tzinfo=WARSAW_TZ) for h in holidays_data]

    # Znajdź wszystkie grupy
    groups = sorted(set(c['group'] for c in classes))
    print(f"📋 Znalezione grupy: {groups}\n")
    print(f"🚫 Dni wolne: {len(holidays)}\n")

    # Generuj ICS dla każdej grupy
    output_dir = Path('docs/static/calendars_v2')
    for group_num in groups:
        generate_ics_for_group(
            group_num,
            classes,
            holidays,
            output_dir / f'grupa_{group_num}.ics'
        )

    print(f"\n🎉 Gotowe! Wygenerowano {len(groups)} ulepszonych kalendarzy")
    print(f"📍 Z adresami budynków")
    print(f"📅 Z dokładnymi zakresami dat (np. Historia Med. tylko 24.XI-19.I)")
    print(f"🚫 Bez dni wolnych i świąt")
