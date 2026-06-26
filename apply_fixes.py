#!/usr/bin/env python3
"""Apply translations from fixes.json to words.js"""
import re, json

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

with open("c:/Users/admin/Desktop/vocab-app/fixes.json", "r", encoding="utf-8") as f:
    fixes = json.load(f)

fixed = 0
not_found = []
for w in data:
    h = w["h"]
    if h in fixes:
        w["e"] = fixes[h]
        fixed += 1

# Verify no suspects remain
meaning_map = {}
for w in data:
    meaning_map[w["h"].lower()] = w["e"]

remaining = []
for i, w in enumerate(data):
    h = w["h"].lower()
    e = w["e"]
    for j in range(1, len(h)):
        prefix = h[:j]
        if prefix in meaning_map and prefix != h:
            if meaning_map[prefix] == e:
                remaining.append((i, w["h"], e, prefix))
                break

print(f"Fixed: {fixed}")
print(f"Remaining suspects: {len(remaining)}")
if remaining:
    print("\nStill need fixing:")
    for idx, h, e, prefix in remaining[:50]:
        print(f"  {h:25s} -> '{e}'  (prefix '{prefix}')")
    if len(remaining) > 50:
        print(f"  ... and {len(remaining) - 50} more")

with open("c:/Users/admin/Desktop/vocab-app/words.js", "w", encoding="utf-8") as f:
    f.write("// Hungarian-English vocabulary database\n")
    f.write(f"// {len(data)} words from 5K.csv\n")
    f.write("const wordDatabase = ")
    f.write(json.dumps(data, ensure_ascii=False, indent=2))
    f.write(";\n")
