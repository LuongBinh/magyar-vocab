#!/usr/bin/env python3
"""Second pass: find ALL words with wrong meanings by checking against known-correct word-meaning pairs.
This catches words that weren't caught by the prefix-match detector because the prefix word
has a different spelling (e.g. meg- vs még, le- vs le, etc.)."""
import re, json

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

# Build meaning map
meaning_map = {}
for w in data:
    meaning_map[w["h"].lower()] = w["e"]

# For each word, check if its meaning matches ANY other word's meaning
# where that other word is a prefix of this word (even if different spelling due to accents)
# Also check for words that share the meaning of a short word they start with (case-insensitive, accent-insensitive)

import unicodedata

def strip_accents(s):
    return unicodedata.normalize('NFD', s).replace('\u0300', '').replace('\u0301', '').replace('\u0308', '').replace('\u030c', '')

# Build accent-insensitive prefix map
# For each short word (len <= 4), map its accent-stripped form + meaning to the word
prefix_meanings = {}
for w in data:
    h = w["h"].lower()
    if len(h) <= 5:
        key = strip_accents(h)
        if key not in prefix_meanings:
            prefix_meanings[key] = (h, w["e"])

suspects = []
for i, w in enumerate(data):
    h = w["h"].lower()
    e = w["e"]
    
    # Check all prefixes of this word (accent-insensitive)
    h_stripped = strip_accents(h)
    for j in range(1, min(len(h_stripped), 8)):
        prefix_key = h_stripped[:j]
        if prefix_key in prefix_meanings:
            orig_prefix, prefix_e = prefix_meanings[prefix_key]
            if orig_prefix != h and prefix_e == e:
                suspects.append((i, w["h"], e, orig_prefix, prefix_e))
                break

# Remove duplicates and filter
seen = set()
unique_suspects = []
for s in suspects:
    key = s[1]  # hungarian word
    if key not in seen:
        seen.add(key)
        unique_suspects.append(s)

print(f"Total unique suspects: {len(unique_suspects)}")

# Write to file
with open("c:/Users/admin/Desktop/vocab-app/suspects2.txt", "w", encoding="utf-8") as f:
    f.write(f"Total: {len(unique_suspects)}\n\n")
    for idx, h, e, prefix, prefix_e in unique_suspects:
        f.write(f"{h}|{e}|{prefix}\n")

# Show first 50
for idx, h, e, prefix, prefix_e in unique_suspects[:50]:
    print(f"  [{idx:4d}] {h:25s} -> '{e}'  (prefix '{prefix}')")
if len(unique_suspects) > 50:
    print(f"  ... and {len(unique_suspects) - 50} more")
