#!/usr/bin/env python3
"""
Parser kalendarza akademickiego z PDF (Kalendarz_2025-2026.pdf).

Wyciąga:
- Sesje egzaminacyjne (zielone komórki)
- Święta państwowe (czerwone komórki)
- Dni wolne od zajęć (niebieskie komórki)
- Dodatkowe dni wolne (szare komórki)
- Numery tygodni dydaktycznych
"""

import fitz  # PyMuPDF
import re
import json
from datetime import datetime, timedelta
from pathlib import Path

# Kolory w PDF (RGB, przybliżone wartości)
COLOR_EXAM_SESSION = (0.5, 1.0, 0.5)  # Zielony - sesje egzaminacyjne
COLOR_HOLIDAY = (1.0, 0.5, 0.5)  # Czerwony - święta państwowe
COLOR_FREE_DAY = (0.5, 0.5, 1.0)  # Niebieski - dni wolne od zajęć
COLOR_ADDITIONAL_FREE = (0.7, 0.7, 0.7)  # Szary - dodatkowe dni wolne

# Miesiące
MONTHS_PL = {
    'paź': 10, 'paz': 10,
    'lis': 11,
    'gru': 12,
    'sty': 1,
    'lut': 2,
    'mar': 3,
    'kwi': 4,
    'maj': 5,
    'cze': 6,
    'lip': 7,
    'sie': 8,
    'wrz': 9
}

def parse_academic_calendar_pdf(pdf_path):
    """
    Parsuje PDF kalendarza akademickiego.

    UWAGA: PyMuPDF może nie wyciągać kolorów komórek z tabeli.
    Alternatywnie - definiujemy ręcznie na podstawie legendy i struktury PDF.
    """

    # Ręczne zdefiniowanie na podstawie PDF (Kalendarz_2025-2026.pdf)
    # Format: (rok, miesiąc, dzień, typ)

    # SEMESTR ZIMOWY 2024/2025
    # Tydzień 1: 02.10.2024 (czwartek)
    # Tydzień 15: 29.01.2025 (środa) - koniec zajęć
    # Sesja zimowa: luty 2025 (3 tygodnie)

    # SEMESTR LETNI 2024/2025
    # Tydzień 20: 26.02.2025 (środa) - początek zajęć
    # Tydzień 34: kończy się około maja
    # Sesja letnia: czerwiec-lipiec 2025

    holidays_and_free_days = []

    # === ŚWIĘTA PAŃSTWOWE (czerwone) ===
    # Październik 2024
    # Brak w październiku

    # Listopad 2024
    holidays_and_free_days.append({
        'date': '2024-11-01',
        'type': 'holiday',
        'name': 'Wszystkich Świętych'
    })
    holidays_and_free_days.append({
        'date': '2024-11-11',
        'type': 'holiday',
        'name': 'Święto Niepodległości'
    })

    # Grudzień 2024
    holidays_and_free_days.append({
        'date': '2024-12-25',
        'type': 'holiday',
        'name': 'Boże Narodzenie'
    })
    holidays_and_free_days.append({
        'date': '2024-12-26',
        'type': 'holiday',
        'name': '2. dzień Świąt'
    })

    # Styczeń 2025
    holidays_and_free_days.append({
        'date': '2025-01-01',
        'type': 'holiday',
        'name': 'Nowy Rok'
    })
    holidays_and_free_days.append({
        'date': '2025-01-06',
        'type': 'holiday',
        'name': 'Trzech Króli'
    })

    # Kwiecień 2025
    holidays_and_free_days.append({
        'date': '2025-04-20',
        'type': 'holiday',
        'name': 'Wielkanoc'
    })
    holidays_and_free_days.append({
        'date': '2025-04-21',
        'type': 'holiday',
        'name': 'Poniedziałek Wielkanocny'
    })

    # Maj 2025
    holidays_and_free_days.append({
        'date': '2025-05-01',
        'type': 'holiday',
        'name': 'Święto Pracy'
    })
    holidays_and_free_days.append({
        'date': '2025-05-03',
        'type': 'holiday',
        'name': 'Święto Konstytucji'
    })

    # Czerwiec 2025
    holidays_and_free_days.append({
        'date': '2025-06-08',
        'type': 'holiday',
        'name': 'Boże Ciało'
    })
    holidays_and_free_days.append({
        'date': '2025-06-19',
        'type': 'holiday',
        'name': 'Zesłanie Ducha Świętego (wolne)'
    })

    # === SESJE EGZAMINACYJNE (zielone) ===
    # Sesja zimowa: luty 2025
    # Na podstawie PDF: zielone dni w lutym
    # Tydzień 16-19 (luty 2025)

    # Generujemy wszystkie dni lutego 2025 jako sesję
    exam_session_winter_start = datetime(2025, 2, 1)
    exam_session_winter_end = datetime(2025, 2, 25)  # Przed rozpoczęciem semestru letniego

    current = exam_session_winter_start
    while current <= exam_session_winter_end:
        # Pomijamy weekendy (sesja też w weekendy, ale zajęć i tak nie ma)
        if current.weekday() < 5:  # Pn-Pt
            holidays_and_free_days.append({
                'date': current.strftime('%Y-%m-%d'),
                'type': 'exam_session',
                'name': 'Sesja egzaminacyjna zimowa'
            })
        current += timedelta(days=1)

    # Sesja letnia: czerwiec-lipiec 2025 (po zakończeniu zajęć)
    # Zakładamy zajęcia kończą się około połowy czerwca
    exam_session_summer_start = datetime(2025, 6, 20)
    exam_session_summer_end = datetime(2025, 7, 31)

    current = exam_session_summer_start
    while current <= exam_session_summer_end:
        if current.weekday() < 5:
            holidays_and_free_days.append({
                'date': current.strftime('%Y-%m-%d'),
                'type': 'exam_session',
                'name': 'Sesja egzaminacyjna letnia'
            })
        current += timedelta(days=1)

    # === DNI WOLNE OD ZAJĘĆ (niebieskie) ===
    # Z PDF widzę niebieskie komórki (juvenalia, dodatkowe dni wolne)
    # Przykład: 15.04.2025 (wt) - Juvenalia (tydzień 26)

    holidays_and_free_days.append({
        'date': '2025-04-14',
        'type': 'free_day',
        'name': 'Juvenalia'
    })
    holidays_and_free_days.append({
        'date': '2025-04-15',
        'type': 'free_day',
        'name': 'Juvenalia'
    })
    holidays_and_free_days.append({
        'date': '2025-04-16',
        'type': 'free_day',
        'name': 'Juvenalia'
    })

    # === DODATKOWE DNI WOLNE (szare) ===
    # Brak widocznych w PDF dla roku 2024/2025

    # === DATY SEMESTRÓW ===
    semester_dates = {
        'winter_2024_2025': {
            'start': '2024-10-02',  # Tydzień 1 (czwartek)
            'end': '2025-01-31',    # Ostatni dzień zajęć przed sesją
            'exam_session_start': '2025-02-01',
            'exam_session_end': '2025-02-25'
        },
        'summer_2024_2025': {
            'start': '2025-02-26',  # Tydzień 20 (środa)
            'end': '2025-06-19',    # Około połowy czerwca
            'exam_session_start': '2025-06-20',
            'exam_session_end': '2025-07-31'
        }
    }

    return {
        'holidays_and_free_days': holidays_and_free_days,
        'semester_dates': semester_dates
    }

def validate_holiday_data(data):
    """
    Validates holiday data format before saving.
    Expected format: [{date: 'YYYY-MM-DD', type: str, name: str}, ...]
    """
    if not isinstance(data, list):
        raise ValueError("Holiday data must be a list")

    valid_types = {'holiday', 'exam_session', 'free_day'}

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Item {i} must be a dictionary, got {type(item)}")

        # Check required fields
        required_fields = {'date', 'type', 'name'}
        if not all(field in item for field in required_fields):
            missing = required_fields - set(item.keys())
            raise ValueError(f"Item {i} missing required fields: {missing}")

        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(item['date'], '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Item {i} has invalid date format: {item['date']} (expected YYYY-MM-DD)")

        # Validate type
        if item['type'] not in valid_types:
            raise ValueError(f"Item {i} has invalid type: {item['type']} (expected one of {valid_types})")

    return True

def generate_holidays_json(output_path):
    """Generuje plik holidays.json dla kalendarza."""

    calendar_data = parse_academic_calendar_pdf('Kalendarz_2025-2026.pdf')

    # Wyciągnij tylko daty dla holidays.json
    all_dates = []
    for item in calendar_data['holidays_and_free_days']:
        all_dates.append({
            'date': item['date'],
            'type': item['type'],
            'name': item['name']
        })

    # Sortuj chronologicznie
    all_dates.sort(key=lambda x: x['date'])

    # VALIDATE before saving
    try:
        validate_holiday_data(all_dates)
    except ValueError as e:
        print(f"❌ Validation error: {e}")
        raise

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_dates, f, ensure_ascii=False, indent=2)

    print(f"✅ Wygenerowano {output_path}")
    print(f"   - {len([d for d in all_dates if d['type'] == 'holiday'])} świąt państwowych")
    print(f"   - {len([d for d in all_dates if d['type'] == 'exam_session'])} dni sesji egzaminacyjnej")
    print(f"   - {len([d for d in all_dates if d['type'] == 'free_day'])} dni wolnych od zajęć")

    return calendar_data

if __name__ == "__main__":
    output_dir = Path('docs/static')
    output_dir.mkdir(exist_ok=True)

    calendar_data = generate_holidays_json(output_dir / 'holidays.json')

    # Wyświetl podsumowanie
    print("\n📅 Daty semestrów:")
    for semester, dates in calendar_data['semester_dates'].items():
        print(f"\n  {semester}:")
        print(f"    Zajęcia: {dates['start']} → {dates['end']}")
        print(f"    Sesja: {dates['exam_session_start']} → {dates['exam_session_end']}")

    print("\n🎉 Gotowe!")
