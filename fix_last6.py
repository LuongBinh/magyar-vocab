#!/usr/bin/env python3
"""Fix last 6 remaining wrong words"""
import re, json

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

FIXES = {
    "tudtuk": "we knew (it)",
    "tudnod": "you must know",
    "k\u00f6vetett": "he/she followed",
    "h\u00edvsz": "you call",
    "r\u00e9g\u00f3ta": "for a long time",
    "j\u00f6ttek": "they came",
}

for w in data:
    if w["h"] in FIXES:
        old = w["e"]
        w["e"] = FIXES[w["h"]]
        print(f"  {w['h']:15s}  '{old}' -> '{w['e']}'")

with open("c:/Users/admin/Desktop/vocab-app/words.js", "w", encoding="utf-8") as f:
    f.write("// Hungarian-English vocabulary database\n")
    f.write(f"// {len(data)} words from 5K.csv\n")
    f.write("const wordDatabase = ")
    f.write(json.dumps(data, ensure_ascii=False, indent=2))
    f.write(";\n")

print("Done")
