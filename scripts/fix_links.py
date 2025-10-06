#!/usr/bin/env python3
import re

# Read the file
with open('docs/index.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all .md extensions in semestr links with empty string
# Pattern: href="semestr-X/something.md" -> href="semestr-X/something"
content = re.sub(r'href="(semestr-\d+/[^"]+)\.md"', r'href="\1"', content)

# Write back
with open('docs/index.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all links!")
