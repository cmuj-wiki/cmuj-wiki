import requests
from bs4 import BeautifulSoup
import json

# Base URL for syllabus
base_url = "https://sylabus.cm-uj.krakow.pl/pl/8/1/7/1/1"

# Fetch the main page
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Dictionary to store subjects by semester
semesters = {}

# Find all semester tabs (nav-tab-7 through nav-tab-18 for semesters 1-12)
for sem_num in range(1, 13):
    tab_id = f"nav-tab-{sem_num + 6}"  # Semestr 1 starts at nav-tab-7

    print(f"\n=== SEMESTR {sem_num} ===")

    # Find the tab content
    tab_content = soup.find('div', {'id': tab_id})

    if tab_content:
        subjects = []

        # Find all subject entries in the table
        rows = tab_content.find_all('tr')

        for row in rows:
            # Look for subject name in the row
            subject_link = row.find('a', href=True)
            if subject_link:
                subject_name = subject_link.text.strip()
                if subject_name and subject_name not in subjects:
                    subjects.append(subject_name)
                    print(f"  - {subject_name}")

        semesters[f"semestr_{sem_num}"] = subjects
    else:
        print(f"  (Tab not found)")

# Save to JSON file
with open('subjects_by_semester.json', 'w', encoding='utf-8') as f:
    json.dump(semesters, f, ensure_ascii=False, indent=2)

print("\n\nSaved to subjects_by_semester.json")
