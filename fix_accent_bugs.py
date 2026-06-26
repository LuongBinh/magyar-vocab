#!/usr/bin/env python3
"""Fix the 112 accent-insensitive prefix-match bugs"""
import re, json

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

FIXES = {
    # hó (snow) prefix matches
    "hol": "where",
    "honnan": "from where",
    "hova": "where to",
    "hov\u00e1": "where to (formal)",
    "hossz\u00fa": "long",
    "hozott": "he/she brought",
    "hozd": "bring it (imperative)",
    "hozni": "to bring",
    "hozom": "I bring (it)",
    "hozok": "I bring",
    "hozol": "you bring",
    "hozta": "he/she brought (it)",
    "hozt\u00e1k": "they brought (it)",
    "hozt\u00e1l": "you brought (informal)",
    "hozz": "bring (imperative)",
    "hozhatok": "I can bring",
    "hopp\u00e1": "oops; whoa",
    
    # út (road; way) prefix matches
    "ut\u00e1n": "after",
    "utols\u00f3": "last; final",
    "utat": "road/way (accusative)",
    "utolj\u00e1ra": "for the last time; last",
    "ut\u00e1lom": "I hate",
    "ut\u00e1lja": "he/she hates (it)",
    "utc\u00e1n": "on the street",
    "utc\u00e1ra": "onto the street",
    "utaz\u00e1s": "travel; journey",
    "utal": "to transfer; to refer",
    
    # jó (good) prefix matches
    "jobb": "better; right (direction)",
    "john": "John",
    "joey": "Joey",
    
    # már (already) prefix matches
    "marad": "to stay; to remain",
    "marha": "cow; beef; very (slang intensifier)",
    "mark": "Mark",
    "mars": "Mars (planet); go away! (imperative)",
    "martin": "Martin",
    
    # még (still; yet) prefix matches - meg- words
    "megold\u00e1s": "solution",
    "megoldani": "to solve",
    "megoldom": "I solve (it)",
    "megoldjuk": "we solve (it)",
    
    # le (down) prefix matches
    "levelet": "letter (accusative)",
    "lopott": "stolen; he/she stole",
    "Londonban": "in London",
    "lord": "lord",
    "labda": "ball",
    "labd\u00e1t": "ball (accusative)",
    
    # te (you sing.) prefix matches
    "te\u00e1t": "tea (accusative)",
    "tegy\u00e9k": "let them do/put",
    "tegy\u00e9l": "do/put (imperative, informal)",
    "tegy\u00e9tek": "you (plural) did/put",
    
    # kéz (hand) prefix matches
    "kezd": "to begin; to start",
    "kez\u00e9t": "his/her hand (accusative)",
    "keze": "his/her hand",
    "kez\u00e9ben": "in his/her hand",
    
    # kér (asks; requests) prefix matches
    "ker\u00fcl": "to cost; to avoid; to go around",
    "keres": "to search; to look for; to earn",
    "k\u00e9rte": "he/she asked for",
    
    # híd (bridge) prefix matches
    "hideg": "cold",
    "hidd": "believe it (imperative)",
    
    # szó (word) prefix matches
    "szomor\u00fa": "sad",
    "szokott": "usually does; accustomed",
    "szob\u00e1t": "room (accusative)",
    "szob\u00e1ba": "into the room",
    "szob\u00e1j\u00e1ban": "in his/her room",
    "szok\u00e1s": "habit; custom",
    "szokatlan": "unusual; uncommon",
    "szokt\u00e1l": "you usually (do)",
    "szoktak": "they usually (do)",
    "szoktam": "I usually (do)",
    "szoros": "tight; close",
    "szomsz\u00e9d": "neighbor",
    
    # neve (don't - wrong) prefix matches
    "nev\u00e9t": "his/her name (accusative)",
    "nev\u00e9ben": "in his/her name",
    
    # hét (week; seven) prefix matches
    "hete": "his/her week; seventh",
    "heti": "weekly (adjective)",
    
    # víz (water) prefix matches
    "vizet": "water (accusative)",
    "vizsg\u00e1lat": "examination; inspection",
    
    # tudja (knows; can) prefix matches
    "tudj\u00e1k": "they know (it)",
    "tudj\u00e1tok": "you (plural) know (it)",
    "tudt\u00e1k": "they knew (it)",
    "tudt\u00e1l": "you knew (informal)",
    
    # úgy (so; that way) prefix matches
    "ugyan": "indeed; the same",
    "ugye": "right? isn't it?",
    
    # hú (wow) prefix match
    "h\u0171": "loyal; faithful; cool (slang)",
    
    # életét prefix match
    "\u00e9let\u00e9t": "his/her life (accusative)",
    
    # kevés (few; little) prefix matches
    "kevesebb": "less; fewer",
    "keveset": "little; few (accusative)",
    
    # egy (one; a) prefix matches
    "egyel\u0151re": "for now; for the time being",
    
    # irány prefix matches
    "ir\u00e1ny": "direction",
    "ir\u00e1nt": "towards; regarding",
    "iroda": "office",
    "irod\u00e1ba": "into the office",
    "irod\u00e1j\u00e1ban": "in his/her office",
    
    # jegy prefix matches
    "jegyet": "ticket (accusative)",
    
    # jó prefix matches - joga, jogi
    "joga": "his/her right",
    "jogi": "legal (adjective)",
    
    # vér (blood) prefix match
    "verni": "to beat; to hit",
    
    # verseny prefix match
    "verseny": "competition; race",
    
    # varázsló prefix match
    "var\u00e1zsl\u00f3": "wizard; sorcerer",
    "var\u00e1zslat": "magic; spell",
    
    # nehéz prefix matches
    "nehezebb": "more difficult; harder",
    "nehezen": "with difficulty; hardly",
    
    # késő prefix match
    "k\u00e9s\u0151n": "late",
    
    # nő prefix match
    "n\u0151": "woman; to grow",
    
    # False positives (correct as-is):
    # hagyni = to leave; to let (correct, matches hagy)
    # hallani = to hear (correct, matches hall)
    # hitte = he/she believed (correct, matches hitt)
    # hmm = hmm (correct, matches hm)
    # hírek = news (correct, matches hír)
    # sokáig = for a long time (correct, matches soká)
    # evett = he/she ate (correct, matches evés)
    # kérte = he/she asked for (correct, matches kért)
}

# Remove false positives
false_positives = {"hagyni", "hallani", "hitte", "hmm", "h\u00edrek", "sok\u00e1ig", "evett", "k\u00e9rte"}
for fp in false_positives:
    FIXES.pop(fp, None)

fixed = 0
for w in data:
    if w["h"] in FIXES:
        old = w["e"]
        w["e"] = FIXES[w["h"]]
        print(f"  {w['h']:25s}  '{old}' -> '{w['e']}'")
        fixed += 1

print(f"\nFixed {fixed} words")

with open("c:/Users/admin/Desktop/vocab-app/words.js", "w", encoding="utf-8") as f:
    f.write("// Hungarian-English vocabulary database\n")
    f.write(f"// {len(data)} words from 5K.csv\n")
    f.write("const wordDatabase = ")
    f.write(json.dumps(data, ensure_ascii=False, indent=2))
    f.write(";\n")
