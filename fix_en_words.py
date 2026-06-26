#!/usr/bin/env python3
"""Fix 22 words that incorrectly have 'I' as English meaning"""
import re, json

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

# Correct translations for the 22 misassigned words
FIXES = {
    "engem": "me (accusative of én)",
    "ennek": "to this; for this",
    "ennyi": "this much; this many",
    "enyém": "mine",
    "ennyire": "this much (to this extent)",
    "ennél": "than this; at this",
    "ennyit": "this much (accusative)",
    "engedd": "let it; allow it (imperative)",
    "enni": "to eat",
    "engedj": "let; allow (imperative)",
    "engedje": "let him/her; allow (imperative)",
    "engedélyt": "permission (accusative)",
    "energia": "energy",
    "enyémet": "mine (accusative)",
    "engedjen": "let him/her (imperative)",
    "energiát": "energy (accusative)",
    "engedély": "permission; permit",
    "engedjenek": "let them (imperative)",
    "engedem": "I let; I allow",
    "engedi": "he/she lets; allows",
    "engedhetem": "I can let; I can allow",
    "engedjék": "let them (imperative, definite)",
}

fixed = 0
for w in data:
    h = w["h"]
    if h in FIXES:
        old = w["e"]
        w["e"] = FIXES[h]
        print(f"  {h:20s}  '{old}' -> '{w['e']}'")
        fixed += 1

print(f"\nFixed {fixed} words")

with open("c:/Users/admin/Desktop/vocab-app/words.js", "w", encoding="utf-8") as f:
    f.write("// Hungarian-English vocabulary database\n")
    f.write(f"// {len(data)} words from 5K.csv\n")
    f.write("const wordDatabase = ")
    f.write(json.dumps(data, ensure_ascii=False, indent=2))
    f.write(";\n")
