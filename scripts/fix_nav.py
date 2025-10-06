#!/usr/bin/env python3
"""Fix navigation indentation in mkdocs.yml"""

import re

with open('mkdocs.yml', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the nav section
nav_start = content.find('nav:')
nav_end = content.find('\nrepo_url:', nav_start)

before_nav = content[:nav_start]
after_nav = content[nav_end:]
nav_content = content[nav_start:nav_end]

# Fix the pattern: when we see "- Rok" followed by "- rok-X/index.md", indent the index
nav_fixed = re.sub(
    r'(\n    - Rok [IVX]+:)\n(    - rok-\d+/index\.md)',
    r'\1\n      \2',
    nav_content
)

# Fix all subjects under each year to have proper indentation
# Pattern: after "rok-X/index.md", all following lines until next "Rok" should be indented
lines = nav_fixed.split('\n')
output_lines = []
in_year = False
year_indent_level = 0

for i, line in enumerate(lines):
    # Check if this is a year header
    if '- Rok' in line and ':' in line and 'rok-' not in line:
        in_year = True
        year_indent_level = len(line) - len(line.lstrip())
        output_lines.append(line)
    # Check if we're leaving the Studia section
    elif line.strip().startswith('- Prowadzący:') or line.strip().startswith('- Egzaminy:') or line.strip().startswith('- Zasoby:') or line.strip().startswith('- Pomoc:'):
        in_year = False
        output_lines.append(line)
    # If we're in a year section and this is a subject line
    elif in_year and line.strip().startswith('- ') and 'rok-' in line and '/index.md' not in line:
        # Make sure it's indented under the year (2 more spaces)
        stripped = line.lstrip()
        new_line = ' ' * (year_indent_level + 6) + stripped
        output_lines.append(new_line)
    else:
        output_lines.append(line)

nav_fixed = '\n'.join(output_lines)

# Reconstruct the file
result = before_nav + nav_fixed + after_nav

with open('mkdocs.yml', 'w', encoding='utf-8') as f:
    f.write(result)

print("✅ Navigation fixed!")
