#!/usr/bin/env python3
"""Fix nekem and any other remaining wrong words"""
import re, json

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

FIXES = {
    "nekem": "to me; for me",
    "neki": "to him/her; for him/her",
    "neked": "to you; for you",
    "nektek": "to you (plural); for you (plural)",
    "nekik": "to them; for them",
    "nekünk": "to us; for us",
}

# Check current meanings
for w in data:
    if w["h"] in FIXES:
        print(f"  {w['h']:15s}  '{w['e']}' -> '{FIXES[w['h']]}'")
        w["e"] = FIXES[w["h"]]

with open("c:/Users/admin/Desktop/vocab-app/words.js", "w", encoding="utf-8") as f:
    f.write("// Hungarian-English vocabulary database\n")
    f.write(f"// {len(data)} words from 5K.csv\n")
    f.write("const wordDatabase = ")
    f.write(json.dumps(data, ensure_ascii=False, indent=2))
    f.write(";\n")

print("\nDone")
