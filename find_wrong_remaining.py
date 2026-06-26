#!/usr/bin/env python3
"""Find all remaining wrong-meaning words and output them for fixing.
Approach: for each word, if its meaning exactly matches a known short word's meaning,
and the word is NOT a legitimate form of that short word, flag it."""
import re, json

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

# All wrong words from audit_exact.py output, organized by what they currently say
wrong_words = set()
for w in data:
    h = w["h"]
    e = w["e"]
    # Flag words with known-wrong meanings
    wrong_meanings = {
        "don't", "no; not", "yes", "what; we", "if", "today", "and",
        "also; too", "this", "I (pronoun)", "here", "there",
        "you (sing.)", "the; that", "one; a", "but", "or",
        "is; there is", "only; just", "is needed; must",
        "already", "still; yet", "very", "now",
        "more", "good", "bad", "big", "small",
        "who; out", "gives", "tooth", "hand", "head",
        "eye", "water", "salt", "snow", "stone",
        "bed", "horse", "color", "lake", "wind; edge",
        "blood", "maybe", "down", "up", "road; way",
        "street", "wall", "writes", "asks; requests",
        "loves; likes", "buys; takes", "thanks",
        "day; sun", "person", "piece", "package",
        "morning", "movie", "young", "child", "news",
        "pity; shame", "a lot; bunch", "exists",
        "in a year", "others", "how much (acc.)",
        "let's do it", "damn it", "with which (relative)",
        "I will tell; I will say", "my daughter",
        "he/she called", "busy", "clearly", "stinky",
        "wow", "face", "I call you", "pain",
        "as much as", "I looked", "luck", "this way",
        "federal", "building", "you took", "they bought",
        "wishes", "to the side", "stand (plural, imper.)",
        "shining", "method", "to the police",
        "he/she followed", "on the spot", "you have fun",
        "its essence", "hole (acc.)", "he/she can wait",
        "in a form", "they came", "cheerful",
        "your mother", "right; correct", "lasting; holding",
        "will be", "you call", "glance (acc.)",
        "villain", "special", "dry", "my part",
        "our choice", "tree", "defense (adjective)",
        "my business (none of)", "speaking; about",
        "to a girl", "on them", "date", "pilot",
        "I ate", "he/she asks for", "in hell",
        "he/she obtained", "mother (acc.)", "knows; can",
        "leg; foot", "ice", "writer", "waits; castle",
        "year", "week; seven",
    }
    
    if e in wrong_meanings:
        # Check if this word is the legitimate owner of this meaning
        # by checking if it's in the known-correct list
        pass

# Instead, let's just find all words that share meanings with short words
# Build map: meaning -> list of words with that meaning
meaning_to_words = {}
for w in data:
    e = w["e"]
    if e not in meaning_to_words:
        meaning_to_words[e] = []
    meaning_to_words[e].append(w["h"])

# For each meaning, if there are multiple words, check which ones are wrong
# by looking at whether the word is a known correct owner
KNOWN_CORRECT = {
    "ne", "nem", "igen", "mi", "ha", "ma", "és", "is", "ez", "én",
    "itt", "ott", "te", "az", "egy", "de", "vagy", "van", "csak",
    "kell", "már", "még", "nagyon", "most", "több", "jó", "rossz",
    "nagy", "kicsi", "kis", "ki", "ad", "fog", "kéz", "fej", "szem",
    "víz", "só", "hó", "kő", "ágy", "ló", "szín", "tó", "szél", "vér",
    "talán", "le", "fel", "út", "utca", "fal", "ír", "kér", "szeret",
    "vesz", "kösz", "nap", "ember", "darab", "csomag", "reggel",
    "film", "fiatal", "gyerek", "hír", "kár", "csomó", "létezik",
    "évben", "mások", "mennyit", "csináljuk", "bassza", "amivel",
    "elmondom", "lányom", "hívott", "elfoglalt", "tisztán", "büdös",
    "hűha", "arc", "hívlak", "fájdalom", "amennyire", "néztem",
    "szerencse", "errefelé", "szövetségi", "épület", "vetted",
    "vettek", "kíván", "oldalra", "álljatok", "ragyogó", "módszer",
    "rendőrségnek", "követte", "helyben", "szórakozol", "lényege",
    "lyukat", "várhat", "formában", "eljöttek", "vidám",
    "édesanyád", "tartó", "lesz", "hívod", "pillantást",
    "gazember", "speciális", "száraz", "részem", "választásunk",
    "fa", "védelmi", "közöm", "szóló", "lánynak", "rajtuk",
    "randi", "pilóta", "ettem", "kéri", "pokolban", "szerzett",
    "anyát", "tud", "labda", "jegy", "iroda", "varázsló", "vár",
    "év", "hét", "szó", "híd", "no", "úgy", "neve", "kevés",
    "élete", "evés", "kért", "hitt", "hm", "soká", "hagy",
    "hall", "keres", "kerül", "kezd", "marad", "tudja",
}

# Also add legitimate derivatives (infinitives, conjugations)
LEGITIMATE_DERIVATIVES = {
    "hagyni", "hallani", "hitte", "hmm", "hírek", "sokáig", "evett",
    "kérte", "maradni", "keresni", "kezdeni", "kerülni",
    "tudják", "tudjátok", "tudták", "tudtál",
    "életét", "kevesebb", "keveset", "hete", "heti",
    "vizet", "vizsgálat", "szomorú", "szokott", "szobát",
    "szobába", "szobájában", "szokás", "szokatlan",
    "szoktál", "szoktak", "szoktam", "szoros", "szomszéd",
    "hideg", "hidd", "kezd", "kezét", "keze", "kezében",
    "kerül", "keres", "nevét", "nevében",
    "után", "utolsó", "utat", "utoljára", "utálom", "utálja",
    "utcán", "utcára", "utazás", "utal",
    "jobb", "john", "joey", "joga", "jogi",
    "marha", "mark", "mars", "martin",
    "hol", "honnan", "hova", "hov\u00e1", "hossz\u00fa",
    "hozott", "hozd", "hozni", "hozom", "hozok", "hozol",
    "hozta", "hozt\u00e1k", "hozt\u00e1l", "hozz", "hozhatok",
    "hopp\u00e1", "h\u0171",
    "ugyan", "ugye",
    "egyel\u0151re", "egyesek", "egyetlen",
    "ir\u00e1ny", "ir\u00e1nt", "iroda", "irod\u00e1ba", "irod\u00e1j\u00e1ban",
    "jegyet", "levelet", "lopott", "Londonban", "lord",
    "labda", "labd\u00e1t",
    "te\u00e1t", "tegy\u00e9k", "tegy\u00e9l", "tegy\u00e9tek",
    "verni", "verseny", "var\u00e1zsl\u00f3", "var\u00e1zslat",
    "nehezebb", "nehezen", "k\u00e9s\u0151n",
    "n\u0151", "hotel", "ut\u00f3bb",
    "megold\u00e1s", "megoldani", "megoldom", "megoldjuk",
    "emberek",
}

ALL_OK = KNOWN_CORRECT | LEGITIMATE_DERIVATIVES

# Find words with wrong meanings
wrong = []
for w in data:
    h = w["h"]
    e = w["e"]
    if e in meaning_to_words and len(meaning_to_words[e]) > 0:
        # Check if this word is the correct owner
        if h not in ALL_OK:
            # Check if any known-correct word has this meaning
            correct_owners = [x for x in meaning_to_words[e] if x in KNOWN_CORRECT]
            if correct_owners and h != correct_owners[0]:
                wrong.append((h, e, correct_owners[0]))

# Write to file
with open("c:/Users/admin/Desktop/vocab-app/wrong_remaining.txt", "w", encoding="utf-8") as f:
    f.write(f"Total: {len(wrong)}\n\n")
    for h, e, correct in wrong:
        f.write(f"{h}|{e}|{correct}\n")

print(f"Total wrong remaining: {len(wrong)}")
for h, e, correct in wrong[:30]:
    print(f"  {h:25s} -> '{e}'  (should be like '{correct}')")
if len(wrong) > 30:
    print(f"  ... and {len(wrong) - 30} more")
