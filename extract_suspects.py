#!/usr/bin/env python3
"""Extract all suspect words to a simple list file"""
import re, json

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

meaning_map = {}
for w in data:
    meaning_map[w["h"].lower()] = w["e"]

suspects = []
for i, w in enumerate(data):
    h = w["h"].lower()
    e = w["e"]
    for j in range(1, len(h)):
        prefix = h[:j]
        if prefix in meaning_map and prefix != h:
            if meaning_map[prefix] == e:
                suspects.append(w["h"])
                break

with open("c:/Users/admin/Desktop/vocab-app/need_fix.txt", "w", encoding="utf-8") as f:
    for s in suspects:
        f.write(s + "\n")

print(f"Total: {len(suspects)}")
