#!/usr/bin/env python3
"""
Smart Subject Page Updater

Updates subject pages with official data from YAML files while preserving
student-contributed content using marker-based sections.

Usage:
    python3 scripts/update_subject_pages.py [--subject SLUG] [--all]
"""

import yaml
import argparse
import re
from pathlib import Path
from datetime import datetime

# Paths
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data" / "subjects"
DOCS_DIR = ROOT_DIR / "docs"

def load_subject_data(slug):
    """Load YAML data for a subject"""
    yaml_file = DATA_DIR / f"{slug}.yml"
    if not yaml_file.exists():
        print(f"❌ YAML file not found: {yaml_file}")
        return None

    with open(yaml_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def find_subject_markdown(slug, semester):
    """Find the markdown file for a subject"""
    md_file = DOCS_DIR / f"semestr-{semester}" / f"{slug}.md"
    if not md_file.exists():
        print(f"⚠️  Markdown file not found: {md_file}")
        return None
    return md_file

def find_related_subjects(data):
    """Find all subjects in the same subject_group"""
    subject_group = data.get('subject_group')
    if not subject_group:
        return []

    related = []
    yaml_files = list(DATA_DIR.glob("*.yml"))

    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            other_data = yaml.safe_load(f)

        if other_data.get('subject_group') == subject_group:
            related.append({
                'slug': other_data.get('slug'),
                'name': other_data.get('name'),
                'semester': other_data.get('semester'),
                'subject_part': other_data.get('subject_part', 1),
                'file': yaml_file.stem
            })

    # Sort by subject_part
    return sorted(related, key=lambda x: x['subject_part'])

def generate_multi_semester_navigation(data, related_subjects):
    """Generate navigation for multi-semester subjects"""
    if not data.get('subject_group') or len(related_subjects) <= 1:
        return None

    current_part = data.get('subject_part', 1)
    total_parts = data.get('total_parts', 1)

    content = []
    content.append("")
    content.append("!!! info \"Przedmiot wielosemestralny\"")

    # Main message
    if data.get('continues_in_semester'):
        next_sem = data['continues_in_semester']
        content.append(f"    Ten przedmiot jest kontynuowany w semestrze {next_sem}.")
    elif data.get('previous_semester'):
        prev_sem = data['previous_semester']
        content.append(f"    Ten przedmiot jest kontynuacją materiału z semestru {prev_sem}.")
    else:
        content.append(f"    To jest część {current_part}/{total_parts} przedmiotu {data['subject_group']}.")

    content.append("")
    content.append("    **Wszystkie części:**  ")

    # Navigation links
    for subj in related_subjects:
        part_num = subj['subject_part']
        semester = subj['semester']

        if part_num == current_part:
            # Current part - bold, no link
            content.append(f"    **Część {part_num}** (Semestr {semester}) • ")
        else:
            # Other parts - linked
            link = f"../semestr-{semester}/{subj['slug']}.md"
            content.append(f"    [Część {part_num}]({link}) (Semestr {semester}) • ")

    # Remove trailing bullet
    if content[-1].endswith(" • "):
        content[-1] = content[-1][:-3]

    content.append("")

    return "\n".join(content)

def generate_cover_image_section(data):
    """Generate cover image display if available"""
    cover_image = data.get('cover_image')
    if not cover_image:
        return None

    # Check if image file exists
    image_path = ROOT_DIR / "docs" / cover_image
    if not image_path.exists():
        return None

    content = []
    content.append("")
    content.append(f'<div align="center" style="margin: 2rem 0;">')
    content.append(f'  <img src="../{cover_image}" alt="{data["name"]}" style="width: 200px; height: 200px; object-fit: cover; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />')
    content.append(f'</div>')
    content.append("")

    return "\n".join(content)

def generate_medbox_section_content(data):
    """Generate MedBox section content (without markers) for embedding in official section"""
    medbox = data.get('medbox', {})
    if not medbox or not medbox.get('resources'):
        return None

    content = []
    content.append("## 📚 Zasoby MedBox")
    content.append("")
    content.append("!!! info \"MedBox - Zewnętrzne zasoby\"")
    content.append("    Poniższe linki prowadzą do materiałów hostowanych na Google Drive (MedBox).")
    content.append("    [Więcej o MedBox →](../zasoby/medbox-info.md)")
    content.append("")

    resources = medbox.get('resources', {})

    for category, items in resources.items():
        # Category header
        category_names = {
            'ksiazki': '📖 Podręczniki i książki',
            'szpilki': '📌 Preparaty (egzamin praktyczny)',
            'prezentacje': '📊 Prezentacje z wykładów',
            'skrypty': '📝 Skrypty i notatki',
            'embriologia': '🧬 Embriologia',
            'bazy': '💾 Bazy danych',
            'wyklady': '🎓 Wykłady',
            'kolokwia': '📝 Pytania z kolokwiów',
            'cwiczenia': '⚗️ Materiały do ćwiczeń',
            'preparaty': '🔬 Preparaty mikroskopowe',
            'atlasy': '🗺️ Atlasy'
        }

        header = category_names.get(category, category.title())
        content.append(f"### {header}")
        content.append("")

        if isinstance(items, list):
            for item in items:
                title = item.get('title', 'Materiał')
                url = item.get('url', '#')
                desc = item.get('description', '')

                if desc:
                    content.append(f"- **[{title}]({url})**")
                    content.append(f"  <br>*{desc}*")
                else:
                    content.append(f"- [{title}]({url})")

        content.append("")

    # Main MedBox folder link (inline, not as separate section)
    if medbox.get('folder_main'):
        label = medbox.get('folder_main_label', f"Pełny folder MedBox - {data['name']}")
        content.append(f"**[📦 {label}]({medbox['folder_main']})**")
        content.append("")

    return content

def generate_official_section(data):
    """Generate the auto-generated official information section"""

    syllabus = data.get('syllabus', {})
    medbox = data.get('medbox', {})
    kolokwia = data.get('kolokwia', [])

    content = []
    content.append("<!-- START: AUTO-GENERATED-OFFICIAL -->")
    content.append(f"<!-- Auto-generated from data/subjects/{data['slug']}.yml -->")
    content.append(f"<!-- Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->")
    content.append(f"<!-- DO NOT EDIT THIS SECTION MANUALLY -->")
    content.append("")

    # Add cover image if available
    cover_section = generate_cover_image_section(data)
    if cover_section:
        content.append(cover_section)

    content.append("## 📋 Informacje o przedmiocie")
    content.append("")

    # Official data as definition list
    if syllabus.get('ects'):
        content.append(f"**ECTS:** {syllabus['ects']}")
        content.append("")

    coord = syllabus.get('coordinator', {})
    if coord.get('name'):
        coord_str = coord['name']
        if coord.get('email'):
            coord_str += f" ([{coord['email']}](mailto:{coord['email']}))"
        content.append(f"**Koordynator:** {coord_str}")
        content.append("")

    hours = syllabus.get('hours', {})
    if hours.get('total'):
        hours_parts = []
        if hours.get('wyklady'):
            hours_parts.append(f"Wykłady: {hours['wyklady']}h")
        if hours.get('cwiczenia'):
            hours_parts.append(f"Ćwiczenia: {hours['cwiczenia']}h")
        if hours.get('seminaria'):
            hours_parts.append(f"Seminaria: {hours['seminaria']}h")

        hours_str = ", ".join(hours_parts) if hours_parts else f"{hours['total']}h"
        content.append(f"**Godziny:** {hours_str}")
        content.append("")

    if syllabus.get('exam_type'):
        content.append(f"**Forma zaliczenia:** {syllabus['exam_type']}")
        content.append("")

    content.append("")

    # MedBox section (moved to top priority position)
    medbox_content = generate_medbox_section_content(data)
    if medbox_content:
        content.extend(medbox_content)

    # Harmonogram classes table with enhanced UX and dynamic status
    harmonogram_classes = data.get('harmonogram_classes', [])
    if harmonogram_classes and harmonogram_classes[0].get('date') != 'TBD':
        content.append("### 📅 Harmonogram zajęć - Semestr 1")
        content.append("")
        content.append('<table id="harmonogram-table">')
        content.append("  <thead>")
        content.append("    <tr>")
        content.append("      <th>Status</th>")
        content.append("      <th>#</th>")
        content.append("      <th>Data</th>")
        content.append("      <th>Typ</th>")
        content.append("      <th>Temat zajęć</th>")
        content.append("    </tr>")
        content.append("  </thead>")
        content.append("  <tbody>")

        for cls in harmonogram_classes:
            num = cls.get('class_number', '')
            date_str = cls.get('date', '')
            topic = cls.get('topic', '')
            time_str = cls.get('time', '')

            # Determine class type from topic
            if 'Wykład' in topic or 'wykład' in topic:
                typ = '📚 Wykład'
            elif '⚡' in topic or 'KOLOKWIUM' in topic or 'Kolokwium' in topic:
                typ = '⚡ Kolokwium'
            elif 'Powtórki' in topic or 'powtórkowe' in topic or 'Seminaria' in topic:
                typ = '🔄 Powtórki'
            else:
                typ = '🔬 Ćwiczenia'

            # Format date with time if available
            date_display = date_str
            if time_str:
                date_display = f"{date_str}<br><small>{time_str}</small>"

            # Add data-date attribute for JavaScript to process
            content.append(f'    <tr data-date="{date_str}">')
            content.append(f'      <td class="status-cell"></td>')
            content.append(f'      <td>{num}</td>')
            content.append(f'      <td>{date_display}</td>')
            content.append(f'      <td>{typ}</td>')
            content.append(f'      <td>{topic}</td>')
            content.append('    </tr>')

        content.append("  </tbody>")
        content.append("</table>")
        content.append("")

        # Add JavaScript for dynamic status calculation
        content.append("<script>")
        content.append("(function() {")
        content.append("  function updateHarmonogramStatus() {")
        content.append("    const table = document.getElementById('harmonogram-table');")
        content.append("    if (!table) return;")
        content.append("")
        content.append("    const today = new Date();")
        content.append("    today.setHours(0, 0, 0, 0);")
        content.append("    const rows = table.querySelectorAll('tbody tr');")
        content.append("    let nextClassFound = false;")
        content.append("")
        content.append("    rows.forEach(row => {")
        content.append("      const dateStr = row.getAttribute('data-date');")
        content.append("      if (!dateStr) return;")
        content.append("")
        content.append("      // Parse date (format: '02-03.10.2025' or '06.10.2025')")
        content.append("      let classDate;")
        content.append("      try {")
        content.append("        if (dateStr.includes('-') && dateStr.includes('.')) {")
        content.append("          // Range like '02-03.10.2025'")
        content.append("          const parts = dateStr.split('.');")
        content.append("          const dayPart = parts[0].split('-')[1] || parts[0].split('-')[0];")
        content.append("          classDate = new Date(parts[2], parts[1] - 1, dayPart);")
        content.append("        } else {")
        content.append("          // Single date like '06.10.2025'")
        content.append("          const parts = dateStr.split('.');")
        content.append("          classDate = new Date(parts[2], parts[1] - 1, parts[0]);")
        content.append("        }")
        content.append("")
        content.append("        const statusCell = row.querySelector('.status-cell');")
        content.append("        if (classDate < today) {")
        content.append("          statusCell.textContent = '✅';")
        content.append("        } else if (!nextClassFound) {")
        content.append("          statusCell.textContent = '▶️';")
        content.append("          nextClassFound = true;")
        content.append("        } else {")
        content.append("          statusCell.textContent = '';")
        content.append("        }")
        content.append("      } catch (e) {")
        content.append("        console.error('Error parsing date:', dateStr, e);")
        content.append("      }")
        content.append("    });")
        content.append("  }")
        content.append("")
        content.append("  // Run on page load")
        content.append("  if (document.readyState === 'loading') {")
        content.append("    document.addEventListener('DOMContentLoaded', updateHarmonogramStatus);")
        content.append("  } else {")
        content.append("    updateHarmonogramStatus();")
        content.append("  }")
        content.append("})();")
        content.append("</script>")
        content.append("")

    # Kolokwia quick links
    egzaminy = data.get('egzaminy', [])
    if kolokwia or egzaminy:
        content.append("### 🎯 Kolokwia i egzaminy")
        content.append("")

        # Display kolokwia
        for kol in kolokwia:
            title = kol.get('title', 'Kolokwium')
            date = kol.get('date', '')
            link = kol.get('link', '')

            if link:
                content.append(f"- [{title}]({link}) - {date}")
            else:
                content.append(f"- {title} - {date}")

        # Display exams
        if egzaminy:
            content.append("")
            for egz in egzaminy:
                title = egz.get('title', 'Egzamin')
                date = egz.get('date', '')
                time = egz.get('time', '')
                link = egz.get('link', '')

                date_display = f"{date}, {time}" if time else date

                if link:
                    content.append(f"- [{title}]({link}) - {date_display}")
                else:
                    content.append(f"- {title} - {date_display}")

        content.append("")
        content.append("[➡️ Zobacz wszystkie kolokwia](../kolokwia/index.md)")
        content.append("")

    # Official links moved to bottom
    content.append("### 📋 Linki oficjalne")
    content.append("")

    links = []
    if syllabus.get('syllabus_pdf'):
        links.append(f"- [📄 Pełny sylabus (PDF)]({syllabus['syllabus_pdf']})")
    if syllabus.get('department_url'):
        links.append(f"- [🏛️ Strona katedry]({syllabus['department_url']})")
    if data.get('harmonogram_url'):
        links.append(f"- [📅 Program zajęć (strona oficjalna)]({data['harmonogram_url']})")

    if links:
        content.extend(links)
    else:
        content.append("*Brak dostępnych linków oficjalnych*")

    content.append("")

    content.append("<!-- END: AUTO-GENERATED-OFFICIAL -->")

    return "\n".join(content)

def generate_medbox_section(data):
    """Generate the MedBox resources section"""
    medbox = data.get('medbox', {})
    if not medbox or not medbox.get('resources'):
        return None

    content = []
    content.append("<!-- START: AUTO-GENERATED-MEDBOX -->")
    content.append(f"<!-- Auto-generated from data/subjects/{data['slug']}.yml -->")
    content.append(f"<!-- Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->")
    content.append("")
    content.append("## 📚 Zasoby MedBox")
    content.append("")
    content.append("!!! info \"MedBox - Zewnętrzne zasoby\"")
    content.append("    Poniższe linki prowadzą do materiałów hostowanych na Google Drive (MedBox).")
    content.append("    [Więcej o MedBox →](../zasoby/medbox-info.md)")
    content.append("")

    resources = medbox.get('resources', {})

    for category, items in resources.items():
        # Category header
        category_names = {
            'ksiazki': '📖 Podręczniki i książki',
            'szpilki': '📌 Preparaty (egzamin praktyczny)',
            'prezentacje': '📊 Prezentacje z wykładów',
            'skrypty': '📝 Skrypty i notatki',
            'embriologia': '🧬 Embriologia',
            'bazy': '💾 Bazy danych',
            'wyklady': '🎓 Wykłady',
            'kolokwia': '📝 Pytania z kolokwiów',
            'cwiczenia': '⚗️ Materiały do ćwiczeń',
            'preparaty': '🔬 Preparaty mikroskopowe',
            'atlasy': '🗺️ Atlasy'
        }

        header = category_names.get(category, category.title())
        content.append(f"### {header}")
        content.append("")

        if isinstance(items, list):
            for item in items:
                title = item.get('title', 'Materiał')
                url = item.get('url', '#')
                desc = item.get('description', '')

                if desc:
                    content.append(f"- **[{title}]({url})**")
                    content.append(f"  <br>*{desc}*")
                else:
                    content.append(f"- [{title}]({url})")

        content.append("")

    if medbox.get('folder_main'):
        content.append("### 🗂️ Wszystkie materiały")
        content.append("")
        content.append(f"[📦 Pełny folder MedBox - {data['name']}]({medbox['folder_main']})")
        content.append("")

    content.append("<!-- END: AUTO-GENERATED-MEDBOX -->")

    return "\n".join(content)

def update_page(md_file, data):
    """Update a subject page with marker-based replacement"""

    # Read existing content
    with open(md_file, 'r', encoding='utf-8') as f:
        existing_content = f.read()

    # Generate official section (now includes MedBox)
    official_section = generate_official_section(data)

    # Generate multi-semester navigation
    related_subjects = find_related_subjects(data)
    nav_section = generate_multi_semester_navigation(data, related_subjects)
    if nav_section:
        official_section += "\n" + nav_section

    # Replace official section
    pattern_official = r'<!-- START: AUTO-GENERATED-OFFICIAL -->.*?<!-- END: AUTO-GENERATED-OFFICIAL -->'

    if re.search(pattern_official, existing_content, re.DOTALL):
        # Replace existing section
        new_content = re.sub(pattern_official, official_section, existing_content, flags=re.DOTALL)
        print(f"  ✓ Updated existing official section")
    else:
        # Insert after title (first line)
        lines = existing_content.split('\n')
        title_line = lines[0] if lines else f"# {data['name']}"

        new_lines = [title_line, ""]
        new_lines.append(official_section)
        new_lines.append("")
        new_lines.extend(lines[1:])

        new_content = '\n'.join(new_lines)
        print(f"  ✓ Inserted new official section")

    # Remove old standalone MedBox section if it exists (now part of official section)
    pattern_medbox = r'<!-- START: AUTO-GENERATED-MEDBOX -->.*?<!-- END: AUTO-GENERATED-MEDBOX -->'
    if re.search(pattern_medbox, new_content, re.DOTALL):
        new_content = re.sub(pattern_medbox, '', new_content, flags=re.DOTALL)
        print(f"  ✓ Removed old standalone MedBox section (now integrated)")

    # Write updated content
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✅ Saved: {md_file}")

def main():
    parser = argparse.ArgumentParser(description="Update subject pages with YAML data")
    parser.add_argument('--subject', help="Subject slug to update (e.g., anatomia)")
    parser.add_argument('--all', action='store_true', help="Update all subjects with YAML files")

    args = parser.parse_args()

    print("="*60)
    print("Subject Page Updater")
    print("="*60)

    if args.all:
        # Update all subjects with YAML files
        yaml_files = list(DATA_DIR.glob("*.yml"))
        print(f"\nFound {len(yaml_files)} YAML files\n")

        for yaml_file in yaml_files:
            slug = yaml_file.stem
            print(f"Processing: {slug}")

            data = load_subject_data(slug)
            if not data:
                continue

            semester = data.get('semester', 1)
            md_file = find_subject_markdown(slug, semester)
            if not md_file:
                print(f"  ⚠️  Skipping (no markdown file found)")
                continue

            update_page(md_file, data)
            print()

    elif args.subject:
        # Update single subject
        slug = args.subject
        print(f"\nProcessing: {slug}\n")

        data = load_subject_data(slug)
        if not data:
            return

        semester = data.get('semester', 1)
        md_file = find_subject_markdown(slug, semester)
        if not md_file:
            return

        update_page(md_file, data)

    else:
        print("\n❌ Error: Specify --subject SLUG or --all")
        parser.print_help()

    print("\n" + "="*60)
    print("✅ Update complete!")
    print("="*60)

if __name__ == "__main__":
    main()
