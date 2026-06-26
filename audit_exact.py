#!/usr/bin/env python3
"""Find all words with obviously wrong English meanings by checking against known-correct mappings.
Focus on words that got assigned meanings of unrelated short words."""
import re, json

with open("c:/Users/admin/Desktop/vocab-app/words.js", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const wordDatabase = (.+);', text, re.DOTALL)
data = json.loads(m.group(1))

# Check for words where the meaning is clearly wrong
# by looking for known bad assignments
suspects = []
for i, w in enumerate(data):
    h = w["h"]
    e = w["e"]
    
    # "don't" should only be for "ne" (the Hungarian negative imperative)
    if e == "don't" and h != "ne":
        suspects.append((i, h, e, "WRONG - 'don't' should only be 'ne'"))
    
    # "no; not" should only be for "nem"
    if e == "no; not" and h != "nem":
        suspects.append((i, h, e, "WRONG - 'no; not' should only be 'nem'"))
    
    # "yes" should only be for "igen"
    if e == "yes" and h != "igen":
        suspects.append((i, h, e, "WRONG - 'yes' should only be 'igen'"))
    
    # "what; we" should only be for "mi"
    if e == "what; we" and h != "mi":
        suspects.append((i, h, e, "WRONG - 'what; we' should only be 'mi'"))
    
    # "if" should only be for "ha"
    if e == "if" and h != "ha":
        suspects.append((i, h, e, "WRONG - 'if' should only be 'ha'"))
    
    # "today" should only be for "ma"
    if e == "today" and h != "ma":
        suspects.append((i, h, e, "WRONG - 'today' should only be 'ma'"))
    
    # "and" should only be for "és"
    if e == "and" and h != "és":
        suspects.append((i, h, e, "WRONG - 'and' should only be 'és'"))
    
    # "also; too" should only be for "is"
    if e == "also; too" and h != "is":
        suspects.append((i, h, e, "WRONG - 'also; too' should only be 'is'"))
    
    # "this" should only be for "ez"
    if e == "this" and h != "ez":
        suspects.append((i, h, e, "WRONG - 'this' should only be 'ez'"))
    
    # "I (pronoun)" should only be for "én"
    if e == "I (pronoun)" and h != "én":
        suspects.append((i, h, e, "WRONG - 'I' should only be 'én'"))
    
    # "here" should only be for "itt"
    if e == "here" and h != "itt":
        suspects.append((i, h, e, "WRONG - 'here' should only be 'itt'"))
    
    # "there" should only be for "ott"
    if e == "there" and h != "ott":
        suspects.append((i, h, e, "WRONG - 'there' should only be 'ott'"))
    
    # "you (sing.)" should only be for "te"
    if e == "you (sing.)" and h != "te":
        suspects.append((i, h, e, "WRONG - 'you (sing.)' should only be 'te'"))
    
    # "the; that" should only be for "az"
    if e == "the; that" and h != "az":
        suspects.append((i, h, e, "WRONG - 'the; that' should only be 'az'"))
    
    # "one; a" should only be for "egy"
    if e == "one; a" and h != "egy":
        suspects.append((i, h, e, "WRONG - 'one; a' should only be 'egy'"))
    
    # "but" should only be for "de"
    if e == "but" and h != "de":
        suspects.append((i, h, e, "WRONG - 'but' should only be 'de'"))
    
    # "or" should only be for "vagy"
    if e == "or" and h != "vagy":
        suspects.append((i, h, e, "WRONG - 'or' should only be 'vagy'"))
    
    # "is; there is" should only be for "van"
    if e == "is; there is" and h != "van":
        suspects.append((i, h, e, "WRONG - 'is; there is' should only be 'van'"))
    
    # "only; just" should only be for "csak"
    if e == "only; just" and h != "csak":
        suspects.append((i, h, e, "WRONG - 'only; just' should only be 'csak'"))
    
    # "must" should only be for "kell"
    if e == "is needed; must" and h != "kell":
        suspects.append((i, h, e, "WRONG - 'is needed; must' should only be 'kell'"))
    
    # "with" should only be for "vel" or "-val/-vel"
    if e == "with (short form)" and h != "vel":
        suspects.append((i, h, e, "WRONG - 'with' should only be 'vel'"))
    
    # "already" should only be for "már"
    if e == "already" and h != "már":
        suspects.append((i, h, e, "WRONG - 'already' should only be 'már'"))
    
    # "still; yet" should only be for "még"
    if e == "still; yet" and h != "még":
        suspects.append((i, h, e, "WRONG - 'still; yet' should only be 'még'"))
    
    # "very" should only be for "nagyon"
    if e == "very" and h != "nagyon":
        suspects.append((i, h, e, "WRONG - 'very' should only be 'nagyon'"))
    
    # "now" should only be for "most"
    if e == "now" and h != "most":
        suspects.append((i, h, e, "WRONG - 'now' should only be 'most'"))
    
    # "well" should only be for "hát" or "jól"
    if e == "well" and h not in ("hát", "jól"):
        suspects.append((i, h, e, "WRONG - 'well' should only be 'hát' or 'jól'"))
    
    # "so" should only be for "úgy" or "szóval"
    if e == "so" and h not in ("úgy", "szóval", "tehát"):
        suspects.append((i, h, e, "WRONG - 'so' should only be 'úgy' or 'szóval'"))
    
    # "like" should only be for "mint" or "kedvel"
    if e == "like" and h not in ("mint", "kedvel"):
        suspects.append((i, h, e, "WRONG - 'like' should only be 'mint'"))
    
    # "not" should only be for "nem" or "ne"
    if e == "not" and h not in ("nem", "ne"):
        suspects.append((i, h, e, "WRONG - 'not' should only be 'nem' or 'ne'"))
    
    # "no" should only be for "nem" or "nincs"
    if e == "no" and h not in ("nem", "nincs"):
        suspects.append((i, h, e, "WRONG - 'no' should only be 'nem' or 'nincs'"))
    
    # "more" should only be for "több"
    if e == "more" and h != "több":
        suspects.append((i, h, e, "WRONG - 'more' should only be 'több'"))
    
    # "all" should only be for "mind" or "összes" or "all" (loanword)
    if e == "all" and h not in ("mind", "összes", "all", "minden"):
        suspects.append((i, h, e, "WRONG - 'all' should only be 'mind' or 'összes'"))
    
    # "good" should only be for "jó"
    if e == "good" and h != "jó":
        suspects.append((i, h, e, "WRONG - 'good' should only be 'jó'"))
    
    # "bad" should only be for "rossz"
    if e == "bad" and h != "rossz":
        suspects.append((i, h, e, "WRONG - 'bad' should only be 'rossz'"))
    
    # "big" should only be for "nagy"
    if e == "big" and h != "nagy":
        suspects.append((i, h, e, "WRONG - 'big' should only be 'nagy'"))
    
    # "small" should only be for "kicsi" or "kis"
    if e == "small" and h not in ("kicsi", "kis"):
        suspects.append((i, h, e, "WRONG - 'small' should only be 'kicsi' or 'kis'"))
    
    # "who" should only be for "ki"
    if e == "who" and h != "ki":
        suspects.append((i, h, e, "WRONG - 'who' should only be 'ki'"))
    
    # "who; out" should only be for "ki"
    if e == "who; out" and h != "ki":
        suspects.append((i, h, e, "WRONG - 'who; out' should only be 'ki'"))
    
    # "gives" should only be for "ad"
    if e == "gives" and h != "ad":
        suspects.append((i, h, e, "WRONG - 'gives' should only be 'ad'"))
    
    # "tooth" should only be for "fog"
    if e == "tooth" and h != "fog":
        suspects.append((i, h, e, "WRONG - 'tooth' should only be 'fog'"))
    
    # "hand" should only be for "kéz"
    if e == "hand" and h != "kéz":
        suspects.append((i, h, e, "WRONG - 'hand' should only be 'kéz'"))
    
    # "head" should only be for "fej"
    if e == "head" and h != "fej":
        suspects.append((i, h, e, "WRONG - 'head' should only be 'fej'"))
    
    # "eye" should only be for "szem"
    if e == "eye" and h != "szem":
        suspects.append((i, h, e, "WRONG - 'eye' should only be 'szem'"))
    
    # "water" should only be for "víz"
    if e == "water" and h != "víz":
        suspects.append((i, h, e, "WRONG - 'water' should only be 'víz'"))
    
    # "salt" should only be for "só"
    if e == "salt" and h != "só":
        suspects.append((i, h, e, "WRONG - 'salt' should only be 'só'"))
    
    # "snow" should only be for "hó" or "havazás"
    if e == "snow" and h not in ("hó", "havazás"):
        suspects.append((i, h, e, "WRONG - 'snow' should only be 'hó'"))
    
    # "stone" should only be for "kő"
    if e == "stone" and h != "kő":
        suspects.append((i, h, e, "WRONG - 'stone' should only be 'kő'"))
    
    # "bed" should only be for "ágy"
    if e == "bed" and h != "ágy":
        suspects.append((i, h, e, "WRONG - 'bed' should only be 'ágy'"))
    
    # "horse" should only be for "ló" or "paripa"
    if e == "horse" and h not in ("ló", "paripa"):
        suspects.append((i, h, e, "WRONG - 'horse' should only be 'ló'"))
    
    # "color" should only be for "szín"
    if e == "color" and h != "szín":
        suspects.append((i, h, e, "WRONG - 'color' should only be 'szín'"))
    
    # "lake" should only be for "tó" or "tó"
    if e == "lake" and h != "tó":
        suspects.append((i, h, e, "WRONG - 'lake' should only be 'tó'"))
    
    # "wind; edge" should only be for "szél"
    if e == "wind; edge" and h != "szél":
        suspects.append((i, h, e, "WRONG - 'wind; edge' should only be 'szél'"))
    
    # "blood" should only be for "vér"
    if e == "blood" and h != "vér":
        suspects.append((i, h, e, "WRONG - 'blood' should only be 'vér'"))
    
    # "maybe" should only be for "talán"
    if e == "maybe" and h != "talán":
        suspects.append((i, h, e, "WRONG - 'maybe' should only be 'talán'"))
    
    # "down" should only be for "le" or "lefelé"
    if e == "down" and h not in ("le", "lefelé"):
        suspects.append((i, h, e, "WRONG - 'down' should only be 'le'"))
    
    # "up" should only be for "fel" or "felfelé" or "fel"
    if e == "up" and h not in ("fel", "felfelé", "fel"):
        suspects.append((i, h, e, "WRONG - 'up' should only be 'fel'"))
    
    # "road; way" should only be for "út"
    if e == "road; way" and h != "út":
        suspects.append((i, h, e, "WRONG - 'road; way' should only be 'út'"))
    
    # "street" should only be for "utca"
    if e == "street" and h != "utca":
        suspects.append((i, h, e, "WRONG - 'street' should only be 'utca'"))
    
    # "wall" should only be for "fal"
    if e == "wall" and h != "fal":
        suspects.append((i, h, e, "WRONG - 'wall' should only be 'fal'"))
    
    # "writes" should only be for "ír"
    if e == "writes" and h != "ír":
        suspects.append((i, h, e, "WRONG - 'writes' should only be 'ír'"))
    
    # "asks; requests" should only be for "kér"
    if e == "asks; requests" and h != "kér":
        suspects.append((i, h, e, "WRONG - 'asks; requests' should only be 'kér'"))
    
    # "loves; likes" should only be for "szeret"
    if e == "loves; likes" and h != "szeret":
        suspects.append((i, h, e, "WRONG - 'loves; likes' should only be 'szeret'"))
    
    # "buys; takes" should only be for "vesz"
    if e == "buys; takes" and h != "vesz":
        suspects.append((i, h, e, "WRONG - 'buys; takes' should only be 'vesz'"))
    
    # "thanks" should only be for "kösz"
    if e == "thanks" and h not in ("kösz", "köszönet", "köszi"):
        suspects.append((i, h, e, "WRONG - 'thanks' should only be 'kösz'"))
    
    # "day; sun" should only be for "nap"
    if e == "day; sun" and h != "nap":
        suspects.append((i, h, e, "WRONG - 'day; sun' should only be 'nap'"))
    
    # "person" should only be for "ember" or "személy"
    if e == "person" and h not in ("ember", "személy"):
        suspects.append((i, h, e, "WRONG - 'person' should only be 'ember' or 'személy'"))
    
    # "piece" should only be for "darab"
    if e == "piece" and h != "darab":
        suspects.append((i, h, e, "WRONG - 'piece' should only be 'darab'"))
    
    # "package" should only be for "csomag"
    if e == "package" and h != "csomag":
        suspects.append((i, h, e, "WRONG - 'package' should only be 'csomag'"))
    
    # "morning" should only be for "reggel"
    if e == "morning" and h != "reggel":
        suspects.append((i, h, e, "WRONG - 'morning' should only be 'reggel'"))
    
    # "movie" should only be for "film"
    if e == "movie" and h != "film":
        suspects.append((i, h, e, "WRONG - 'movie' should only be 'film'"))
    
    # "naked" should only be for "meztelen"
    if e == "naked" and h not in ("meztelen", "meztelenül"):
        suspects.append((i, h, e, "WRONG - 'naked' should only be 'meztelen'"))
    
    # "young" should only be for "fiatal"
    if e == "young" and h != "fiatal":
        suspects.append((i, h, e, "WRONG - 'young' should only be 'fiatal'"))
    
    # "child" should only be for "gyerek" or "gyermek"
    if e == "child" and h not in ("gyerek", "gyermek"):
        suspects.append((i, h, e, "WRONG - 'child' should only be 'gyerek' or 'gyermek'"))
    
    # "news" should only be for "hír" or "hírek"
    if e == "news" and h not in ("hír", "hírek"):
        suspects.append((i, h, e, "WRONG - 'news' should only be 'hír' or 'hírek'"))
    
    # "pity; shame" should only be for "kár"
    if e == "pity; shame" and h != "kár":
        suspects.append((i, h, e, "WRONG - 'pity; shame' should only be 'kár'"))
    
    # "a lot; bunch" should only be for "csomó"
    if e == "a lot; bunch" and h != "csomó":
        suspects.append((i, h, e, "WRONG - 'a lot; bunch' should only be 'csomó'"))
    
    # "exists" should only be for "létezik"
    if e == "exists" and h != "létezik":
        suspects.append((i, h, e, "WRONG - 'exists' should only be 'létezik'"))
    
    # "in a year" should only be for "évben"
    if e == "in a year" and h != "évben":
        suspects.append((i, h, e, "WRONG - 'in a year' should only be 'évben'"))
    
    # "others" should only be for "mások"
    if e == "others" and h != "mások":
        suspects.append((i, h, e, "WRONG - 'others' should only be 'mások'"))
    
    # "how much (acc.)" should only be for "mennyit"
    if e == "how much (acc.)" and h != "mennyit":
        suspects.append((i, h, e, "WRONG - 'how much (acc.)' should only be 'mennyit'"))
    
    # "let's do it" should only be for "csináljuk"
    if e == "let's do it" and h != "csináljuk":
        suspects.append((i, h, e, "WRONG - 'let's do it' should only be 'csináljuk'"))
    
    # "damn it" should only be for "bassza" or "basszus"
    if e == "damn it" and h not in ("bassza", "basszus"):
        suspects.append((i, h, e, "WRONG - 'damn it' should only be 'bassza'"))
    
    # "with which (relative)" should only be for "amivel"
    if e == "with which (relative)" and h != "amivel":
        suspects.append((i, h, e, "WRONG - 'with which' should only be 'amivel'"))
    
    # "I will tell; I will say" should only be for "elmondom"
    if e == "I will tell; I will say" and h != "elmondom":
        suspects.append((i, h, e, "WRONG - 'I will tell' should only be 'elmondom'"))
    
    # "my daughter" should only be for "lányom"
    if e == "my daughter" and h != "lányom":
        suspects.append((i, h, e, "WRONG - 'my daughter' should only be 'lányom'"))
    
    # "he/she called" should only be for "hívott"
    if e == "he/she called" and h != "hívott":
        suspects.append((i, h, e, "WRONG - 'he/she called' should only be 'hívott'"))
    
    # "busy" should only be for "elfoglalt"
    if e == "busy" and h != "elfoglalt":
        suspects.append((i, h, e, "WRONG - 'busy' should only be 'elfoglalt'"))
    
    # "clearly" should only be for "tisztán"
    if e == "clearly" and h != "tisztán":
        suspects.append((i, h, e, "WRONG - 'clearly' should only be 'tisztán'"))
    
    # "stinky" should only be for "büdös"
    if e == "stinky" and h != "büdös":
        suspects.append((i, h, e, "WRONG - 'stinky' should only be 'büdös'"))
    
    # "wow" should only be for "hűha" or "hű"
    if e == "wow" and h not in ("hűha", "hű", "hahó"):
        suspects.append((i, h, e, "WRONG - 'wow' should only be 'hűha'"))
    
    # "face" should only be for "arc" or "arcát"
    if e == "face" and h not in ("arc", "arcát"):
        suspects.append((i, h, e, "WRONG - 'face' should only be 'arc'"))
    
    # "I call you" should only be for "hívlak"
    if e == "I call you" and h != "hívlak":
        suspects.append((i, h, e, "WRONG - 'I call you' should only be 'hívlak'"))
    
    # "pain" should only be for "fájdalom"
    if e == "pain" and h != "fájdalom":
        suspects.append((i, h, e, "WRONG - 'pain' should only be 'fájdalom'"))
    
    # "as much as" should only be for "amennyire"
    if e == "as much as" and h != "amennyire":
        suspects.append((i, h, e, "WRONG - 'as much as' should only be 'amennyire'"))
    
    # "I looked" should only be for "néztem"
    if e == "I looked" and h != "néztem":
        suspects.append((i, h, e, "WRONG - 'I looked' should only be 'néztem'"))
    
    # "luck" should only be for "szerencse"
    if e == "luck" and h != "szerencse":
        suspects.append((i, h, e, "WRONG - 'luck' should only be 'szerencse'"))
    
    # "this way" should only be for "errefelé"
    if e == "this way" and h != "errefelé":
        suspects.append((i, h, e, "WRONG - 'this way' should only be 'errefelé'"))
    
    # "federal" should only be for "szövetségi"
    if e == "federal" and h != "szövetségi":
        suspects.append((i, h, e, "WRONG - 'federal' should only be 'szövetségi'"))
    
    # "building" should only be for "épület"
    if e == "building" and h != "épület":
        suspects.append((i, h, e, "WRONG - 'building' should only be 'épület'"))
    
    # "you took" should only be for "vetted"
    if e == "you took" and h != "vetted":
        suspects.append((i, h, e, "WRONG - 'you took' should only be 'vetted'"))
    
    # "they bought" should only be for "vettek"
    if e == "they bought" and h != "vettek":
        suspects.append((i, h, e, "WRONG - 'they bought' should only be 'vettek'"))
    
    # "wishes" should only be for "kíván"
    if e == "wishes" and h != "kíván":
        suspects.append((i, h, e, "WRONG - 'wishes' should only be 'kíván'"))
    
    # "to the side" should only be for "oldalra"
    if e == "to the side" and h != "oldalra":
        suspects.append((i, h, e, "WRONG - 'to the side' should only be 'oldalra'"))
    
    # "stand (plural, imper.)" should only be for "álljatok"
    if e == "stand (plural, imper.)" and h != "álljatok":
        suspects.append((i, h, e, "WRONG - 'stand' should only be 'álljatok'"))
    
    # "shining" should only be for "ragyogó"
    if e == "shining" and h != "ragyogó":
        suspects.append((i, h, e, "WRONG - 'shining' should only be 'ragyogó'"))
    
    # "method" should only be for "módszer"
    if e == "method" and h != "módszer":
        suspects.append((i, h, e, "WRONG - 'method' should only be 'módszer'"))
    
    # "to the police" should only be for "rendőrségnek"
    if e == "to the police" and h != "rendőrségnek":
        suspects.append((i, h, e, "WRONG - 'to the police' should only be 'rendőrségnek'"))
    
    # "he/she followed" should only be for "követte"
    if e == "he/she followed" and h != "követte":
        suspects.append((i, h, e, "WRONG - 'he/she followed' should only be 'követte'"))
    
    # "on the spot" should only be for "helyben"
    if e == "on the spot" and h != "helyben":
        suspects.append((i, h, e, "WRONG - 'on the spot' should only be 'helyben'"))
    
    # "you have fun" should only be for "szórakozol"
    if e == "you have fun" and h != "szórakozol":
        suspects.append((i, h, e, "WRONG - 'you have fun' should only be 'szórakozol'"))
    
    # "its essence" should only be for "lényege"
    if e == "its essence" and h != "lényege":
        suspects.append((i, h, e, "WRONG - 'its essence' should only be 'lényege'"))
    
    # "hole (acc.)" should only be for "lyukat"
    if e == "hole (acc.)" and h != "lyukat":
        suspects.append((i, h, e, "WRONG - 'hole' should only be 'lyukat'"))
    
    # "he/she can wait" should only be for "várhat"
    if e == "he/she can wait" and h != "várhat":
        suspects.append((i, h, e, "WRONG - 'he/she can wait' should only be 'várhat'"))
    
    # "in a form" should only be for "formában"
    if e == "in a form" and h != "formában":
        suspects.append((i, h, e, "WRONG - 'in a form' should only be 'formában'"))
    
    # "they came" should only be for "eljöttek"
    if e == "they came" and h != "eljöttek":
        suspects.append((i, h, e, "WRONG - 'they came' should only be 'eljöttek'"))
    
    # "cheerful" should only be for "vidám"
    if e == "cheerful" and h != "vidám":
        suspects.append((i, h, e, "WRONG - 'cheerful' should only be 'vidám'"))
    
    # "your mother" should only be for "édesanyád"
    if e == "your mother" and h != "édesanyád":
        suspects.append((i, h, e, "WRONG - 'your mother' should only be 'édesanyád'"))
    
    # "right; correct" should only be for "jó" or "igaz" or "jóvá"
    if e == "right; correct" and h not in ("jó", "igaz", "jóvá"):
        suspects.append((i, h, e, "WRONG - 'right; correct' should only be 'jó' or 'igaz'"))
    
    # "lasting; holding" should only be for "tartó"
    if e == "lasting; holding" and h != "tartó":
        suspects.append((i, h, e, "WRONG - 'lasting; holding' should only be 'tartó'"))
    
    # "will be" should only be for "lesz" or "lesz"
    if e == "will be" and h not in ("lesz", "leszek", "lesznek"):
        suspects.append((i, h, e, "WRONG - 'will be' should only be 'lesz'"))
    
    # "you call" should only be for "hívod"
    if e == "you call" and h != "hívod":
        suspects.append((i, h, e, "WRONG - 'you call' should only be 'hívod'"))
    
    # "glance (acc.)" should only be for "pillantást"
    if e == "glance (acc.)" and h != "pillantást":
        suspects.append((i, h, e, "WRONG - 'glance' should only be 'pillantást'"))
    
    # "villain" should only be for "gazember"
    if e == "villain" and h != "gazember":
        suspects.append((i, h, e, "WRONG - 'villain' should only be 'gazember'"))
    
    # "special" should only be for "speciális"
    if e == "special" and h != "speciális":
        suspects.append((i, h, e, "WRONG - 'special' should only be 'speciális'"))
    
    # "dry" should only be for "száraz"
    if e == "dry" and h != "száraz":
        suspects.append((i, h, e, "WRONG - 'dry' should only be 'száraz'"))
    
    # "my part" should only be for "részem"
    if e == "my part" and h != "részem":
        suspects.append((i, h, e, "WRONG - 'my part' should only be 'részem'"))
    
    # "our choice" should only be for "választásunk"
    if e == "our choice" and h != "választásunk":
        suspects.append((i, h, e, "WRONG - 'our choice' should only be 'választásunk'"))
    
    # "maybe" should only be for "talán" or "találod"
    if e == "maybe" and h not in ("talán",):
        suspects.append((i, h, e, "WRONG - 'maybe' should only be 'talán'"))
    
    # "tree" should only be for "fa"
    if e == "tree" and h not in ("fa", "fasza"):
        suspects.append((i, h, e, "WRONG - 'tree' should only be 'fa'"))
    
    # "defense (adjective)" should only be for "védelmi"
    if e == "defense (adjective)" and h != "védelmi":
        suspects.append((i, h, e, "WRONG - 'defense' should only be 'védelmi'"))
    
    # "my business (none of)" should only be for "közöm"
    if e == "my business (none of)" and h != "közöm":
        suspects.append((i, h, e, "WRONG - 'my business' should only be 'közöm'"))
    
    # "speaking; about" should only be for "szóló"
    if e == "speaking; about" and h != "szóló":
        suspects.append((i, h, e, "WRONG - 'speaking; about' should only be 'szóló'"))
    
    # "to a girl" should only be for "lánynak"
    if e == "to a girl" and h != "lánynak":
        suspects.append((i, h, e, "WRONG - 'to a girl' should only be 'lánynak'"))
    
    # "on them" should only be for "rajtuk"
    if e == "on them" and h != "rajtuk":
        suspects.append((i, h, e, "WRONG - 'on them' should only be 'rajtuk'"))
    
    # "date" should only be for "randi" or "dátum"
    if e == "date" and h not in ("randi", "dátum"):
        suspects.append((i, h, e, "WRONG - 'date' should only be 'randi' or 'dátum'"))
    
    # "pilot" should only be for "pilóta"
    if e == "pilot" and h != "pilóta":
        suspects.append((i, h, e, "WRONG - 'pilot' should only be 'pilóta'"))
    
    # "I ate" should only be for "ettem"
    if e == "I ate" and h != "ettem":
        suspects.append((i, h, e, "WRONG - 'I ate' should only be 'ettem'"))
    
    # "he/she asks for" should only be for "kéri"
    if e == "he/she asks for" and h != "kéri":
        suspects.append((i, h, e, "WRONG - 'he/she asks for' should only be 'kéri'"))
    
    # "in hell" should only be for "pokolban"
    if e == "in hell" and h != "pokolban":
        suspects.append((i, h, e, "WRONG - 'in hell' should only be 'pokolban'"))
    
    # "he/she obtained" should only be for "szerzett"
    if e == "he/she obtained" and h != "szerzett":
        suspects.append((i, h, e, "WRONG - 'he/she obtained' should only be 'szerzett'"))
    
    # "mother (acc.)" should only be for "anyát"
    if e == "mother (acc.)" and h != "anyát":
        suspects.append((i, h, e, "WRONG - 'mother (acc.)' should only be 'anyát'"))
    
    # "my daughter" should only be for "lányom"
    if e == "my daughter" and h != "lányom":
        suspects.append((i, h, e, "WRONG - 'my daughter' should only be 'lányom'"))
    
    # "knows; can" should only be for "tud" or "tudtuk"
    if e == "knows; can" and h not in ("tud", "tudtuk"):
        suspects.append((i, h, e, "WRONG - 'knows; can' should only be 'tud'"))

print(f"Total suspects: {len(suspects)}")
for idx, h, e, reason in suspects:
    print(f"  [{idx:4d}] {h:25s} -> '{e}'  {reason}")
