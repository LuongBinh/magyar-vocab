#!/usr/bin/env python3
"""Fix remaining false-positive suspects that actually need different translations"""
import re, json

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

# These need refined translations (plural forms, etc.)
FIXES = {
    "emberek": "people",  # was "person" (singular)
}

fixed = 0
for w in data:
    if w["h"] in FIXES:
        old = w["e"]
        w["e"] = FIXES[w["h"]]
        print(f"  {w['h']:20s}  '{old}' -> '{w['e']}'")
        fixed += 1

print(f"\nFixed {fixed} additional words")

with open("c:/Users/admin/Desktop/vocab-app/words.js", "w", encoding="utf-8") as f:
    f.write("// Hungarian-English vocabulary database\n")
    f.write(f"// {len(data)} words from 5K.csv\n")
    f.write("const wordDatabase = ")
    f.write(json.dumps(data, ensure_ascii=False, indent=2))
    f.write(";\n")
