#!/usr/bin/env python3
"""Audit all words for missing/suspicious English meanings"""
import re, json
from collections import defaultdict

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

issues = []

for i, w in enumerate(data):
    h = w.get("h", "")
    e = w.get("e", "")
    
    if not e:
        issues.append((i, h, "MISSING_E_FIELD", e))
        continue
    if e == "(Hungarian word)":
        issues.append((i, h, "PLACEHOLDER", e))
        continue
    if e.strip() == "":
        issues.append((i, h, "EMPTY", e))
        continue
    if h.lower() == e.strip().lower():
        issues.append((i, h, "SAME_AS_HUNGARIAN", e))
        continue
    if len(e.strip()) < 2:
        issues.append((i, h, "TOO_SHORT", e))
        continue
    if "(Hungarian" in e or "word)" in e:
        issues.append((i, h, "PLACEHOLDER_PATTERN", e))
        continue
    if f"({h})" in e:
        issues.append((i, h, "HUNGARIAN_IN_PARENS", e))
        continue

    # Single word with Hungarian diacritics - might be untranslated
    hungarian_chars = set("áéíóöőúüű")
    words_in_e = e.replace(";", " ").replace(",", " ").replace("/", " ").split()
    if len(words_in_e) == 1 and any(c in hungarian_chars for c in words_in_e[0]):
        issues.append((i, h, "POSSIBLE_UNTRANSLATED", e))

print(f"Total words: {len(data)}")
print(f"Issues found: {len(issues)}")

by_type = defaultdict(list)
for idx, h, issue_type, e in issues:
    by_type[issue_type].append((idx, h, e))

for issue_type, items in sorted(by_type.items()):
    print(f"\n=== {issue_type} ({len(items)} occurrences) ===")
    for idx, h, e in items[:50]:
        print(f"  [{idx}] {h:20s} -> {e}")
    if len(items) > 50:
        print(f"  ... and {len(items) - 50} more")
