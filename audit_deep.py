#!/usr/bin/env python3
"""Deeper audit: check for suspicious translations"""
import re, json
from collections import defaultdict

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

issues = []

# Common Hungarian words that should NOT have certain English meanings
# Check for words where the English meaning seems unrelated
for i, w in enumerate(data):
    h = w.get("h", "").strip()
    e = w.get("e", "").strip()
    
    if not e or len(e) < 2:
        continue
    
    # Check for meanings that are just a single capital letter
    if len(e) == 1 and e.isalpha():
        issues.append((i, h, "SINGLE_CHAR_MEANING", e))
    
    # Check for meanings that contain only Hungarian-specific patterns
    # e.g. "Spoken like" prefix in mnemonic but in meaning field
    if e.startswith("Spoken like") or e.startswith("Sounds like"):
        issues.append((i, h, "MNEMONIC_IN_MEANING", e))
    
    # Check for very long meanings (> 200 chars) - might be corrupted
    if len(e) > 200:
        issues.append((i, h, "VERY_LONG_MEANING", e[:80] + "..."))
    
    # Check for meanings with newlines or tabs
    if "\n" in e or "\t" in e:
        issues.append((i, h, "NEWLINE_IN_MEANING", repr(e[:50])))
    
    # Check for duplicate semicolons or weird punctuation
    if ";;" in e or ",," in e or "//" in e:
        issues.append((i, h, "DUPLICATE_PUNCT", e))
    
    # Check for meanings that are just a number
    if e.replace(".", "").replace(",", "").isdigit():
        issues.append((i, h, "NUMERIC_MEANING", e))

# Also check for words where English meaning is a common English word
# but the Hungarian word is clearly different (potential wrong match)
# Check for words starting with common Hungarian prefixes that got wrong matches
suspicious_prefixes = {
    "meg": "verb prefix meaning 'completely/finishing'",
    "fel": "verb prefix meaning 'up'",
    "el": "verb prefix meaning 'away'",
    "be": "verb prefix meaning 'in'",
    "ki": "verb prefix meaning 'out'",
    "le": "verb prefix meaning 'down'",
    "oda": "verb prefix meaning 'there'",
    "ide": "verb prefix meaning 'here'",
    "vissza": "verb prefix meaning 'back'",
}

print(f"Total words: {len(data)}")
print(f"Issues found: {len(issues)}")

by_type = defaultdict(list)
for idx, h, issue_type, e in issues:
    by_type[issue_type].append((idx, h, e))

for issue_type, items in sorted(by_type.items()):
    print(f"\n=== {issue_type} ({len(items)} occurrences) ===")
    for idx, h, e in items[:30]:
        print(f"  [{idx}] {h:20s} -> {e}")
    if len(items) > 30:
        print(f"  ... and {len(items) - 30} more")

# Also check for potential wrong translations by sampling
# Words where meaning seems too generic or doesn't match
print("\n=== SAMPLING: First 20 words for manual review ===")
for w in data[:20]:
    print(f"  {w['h']:20s} -> {w['e']}")

print("\n=== SAMPLING: Words 1000-1020 ===")
for w in data[1000:1020]:
    print(f"  {w['h']:20s} -> {w['e']}")

print("\n=== SAMPLING: Words 2000-2020 ===")
for w in data[2000:2020]:
    print(f"  {w['h']:20s} -> {w['e']}")

print("\n=== SAMPLING: Words 3000-3020 ===")
for w in data[3000:3020]:
    print(f"  {w['h']:20s} -> {w['e']}")

print("\n=== SAMPLING: Words 4000-4020 ===")
for w in data[4000:4020]:
    print(f"  {w['h']:20s} -> {w['e']}")

print("\n=== SAMPLING: Last 20 words ===")
for w in data[-20:]:
    print(f"  {w['h']:20s} -> {w['e']}")
