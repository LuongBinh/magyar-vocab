#!/usr/bin/env python3
"""Find all prefix-match bugs and output to file for fixing"""
import re, json
from collections import Counter

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
                suspects.append((i, w["h"], e, prefix))
                break

with open("c:/Users/admin/Desktop/vocab-app/suspects.txt", "w", encoding="utf-8") as f:
    f.write(f"Total suspects: {len(suspects)}\n\n")
    for idx, h, e, prefix in suspects:
        f.write(f"{idx}|{h}|{e}|{prefix}\n")

print(f"Total suspects: {len(suspects)}")
print("Written to suspects.txt")

prefix_counts = Counter(prefix for _, _, _, prefix in suspects)
print("\nMost common wrong prefixes:")
for prefix, count in prefix_counts.most_common(20):
    print(f"  '{prefix}' caused {count} wrong matches")
