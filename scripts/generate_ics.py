#!/usr/bin/env python3
"""
Generator plików ICS (kalendarzy) z planu zajęć.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import re
from icalendar import Calendar, Event
from zoneinfo import ZoneInfo

WARSAW_TZ = ZoneInfo("Europe/Warsaw")

# Początek semestru zimowego 2024/2025
SEMESTER_START = datetime(2024, 10, 1, tzinfo=WARSAW_TZ)  # 1 października 2024
SEMESTER_END = datetime(2025, 2, 28, tzinfo=WARSAW_TZ)    # Koniec lutego 2025

def parse_date_range(date_str):
    """
    Parsuje string z datami typu:
    - "3.X.2025"
    - "28.XI - 16.I"
    - "10.X-21.XI"
    Zwraca (start_date, end_date) lub None
    """
    if not date_str:
        return None

    # Mapa miesięcy rzymskich
    months = {
        'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6,
        'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12
    }

    # Próbuj wyciągnąć zakres dat
    # Format: "DD.MM - DD.MM" lub "DD.MM-DD.MM"
    range_pattern = r'(\d{1,2})\.([IVX]+)(?:\.\d{4})?\s*-\s*(\d{1,2})\.([IVX]+)(?:\.\d{4})?'
    match = re.search(range_pattern, date_str)

    if match:
        day1, month1, day2, month2 = match.groups()
        year = 2024 if months[month1] >= 10 else 2025  # Semestr zimowy
        year2 = year if months[month2] >= months[month1] else year + 1

        start = datetime(year, months[month1], int(day1), tzinfo=WARSAW_TZ)
        end = datetime(year2, months[month2], int(day2), tzinfo=WARSAW_TZ)
        return (start, end)

    # Pojedyncza data: "DD.MM.YYYY" lub "DD.MM"
    single_pattern = r'(\d{1,2})\.([IVX]+)(?:\.(\d{4}))?'
    match = re.search(single_pattern, date_str)

    if match:
        day, month, year = match.groups()
        year = int(year) if year else (2024 if months[month] >= 10 else 2025)
        date = datetime(year, months[month], int(day), tzinfo=WARSAW_TZ)
        return (date, date)

    return None

def get_class_dates(cls, semester_start, semester_end):
    """
    Zwraca listę dat kiedy odbywa się dane zajęcie.
    """
    # Jeśli są określone daty w komórce, użyj ich
    if cls.get('dates'):
        date_range = parse_date_range(cls['dates'][0])
        if date_range:
            start, end = date_range
        else:
            # Fallback - cały semestr
            start, end = semester_start, semester_end
    else:
        # Brak dat - zakładamy cały semestr
        start, end = semester_start, semester_end

    # Generuj wszystkie wystąpienia w danym dniu tygodnia
    dates = []
    current = start

    # Przejdź do pierwszego wystąpienia tego dnia tygodnia
    while current.weekday() != cls['day']:
        current += timedelta(days=1)

    # Generuj daty co tydzień
    while current <= end:
        dates.append(current)
        current += timedelta(weeks=1)

    return dates

def generate_ics_for_group(group_num, classes, output_path):
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
    cal.add('x-wr-caldesc', f'Plan zajęć dla grupy {group_num} - I rok Kierunku Lekarskiego UJ CM')

    event_count = 0

    for cls in group_classes:
        # Pobierz wszystkie daty dla tego zajęcia
        dates = get_class_dates(cls, SEMESTER_START, SEMESTER_END)

        for date in dates:
            event = Event()

            # Tytuł wydarzenia
            subject = cls['subject']
            if cls.get('type'):
                subject = f"{subject} ({cls['type']})"

            event.add('summary', subject)

            # Czas rozpoczęcia
            start_time = date.replace(
                hour=cls['hour'] or 8,
                minute=cls['minute'] or 0,
                second=0,
                microsecond=0
            )

            # Zakładamy 90 minut na zajęcia (domyślnie)
            duration = timedelta(minutes=90)
            end_time = start_time + duration

            event.add('dtstart', start_time)
            event.add('dtend', end_time)

            # Lokalizacja
            if cls.get('location'):
                event.add('location', cls['location'])

            # Opis
            description_parts = []
            if cls.get('type'):
                description_parts.append(f"Typ: {cls['type']}")
            if cls.get('dates'):
                description_parts.append(f"Daty: {cls['dates'][0]}")
            if cls.get('time'):
                description_parts.append(f"Godziny: {cls['time']}")

            description_parts.append(f"\nGrupa: {group_num}")
            description_parts.append(f"\n🩺 Wygenerowano przez CMUJ Wiki")

            event.add('description', '\n'.join(description_parts))

            # UID - unikalny identyfikator
            event.add('uid', f"{group_num}-{cls['subject']}-{start_time.isoformat()}@cmuj-wiki")
            event.add('dtstamp', datetime.now(tz=WARSAW_TZ))

            cal.add_component(event)
            event_count += 1

    # Zapisz do pliku
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(cal.to_ical())

    print(f"✅ Grupa {group_num}: {len(group_classes)} zajęć → {event_count} wydarzeń → {output_path}")

if __name__ == "__main__":
    # Wczytaj dane
    with open('docs/static/schedule_data.json', 'r', encoding='utf-8') as f:
        classes = json.load(f)

    # Znajdź wszystkie grupy
    groups = sorted(set(c['group'] for c in classes))
    print(f"📋 Znalezione grupy: {groups}\n")

    # Generuj ICS dla każdej grupy
    output_dir = Path('docs/static/calendars')
    for group_num in groups:
        generate_ics_for_group(
            group_num,
            classes,
            output_dir / f'grupa_{group_num}.ics'
        )

    print(f"\n🎉 Gotowe! Wygenerowano {len(groups)} kalendarzy")
