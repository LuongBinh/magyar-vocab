#!/usr/bin/env python3
"""Generate Hungarian-English vocabulary database from 5K.csv + vocab.js"""

import json, re, os, random

DATA = "C:/Users/admin/Desktop/design_handoff_hungarian_vocab/data"
OUT = "C:/Users/admin/Desktop/vocab-app"

with open(os.path.join(DATA, "5K.csv"), "r", encoding="utf-8") as f:
    csv_words = [l.strip() for l in f if l.strip()]
print(f"5K.csv: {len(csv_words)} words")

with open(os.path.join(DATA, "vocab.js"), "r", encoding="utf-8") as f:
    js = f.read()
pre = {}
for m in re.finditer(r'\{h:"([^"]*)",\s*e:"([^"]*)",\s*m:"([^"]*)"\}', js):
    h, e, mn = m.group(1), m.group(2), m.group(3)
    pre[h] = {"h": h, "e": e, "m": mn}
for m in re.finditer(r'\{h:"([^"]*)"\}', js):
    h = m.group(1)
    if h not in pre:
        pre[h] = {"h": h}
print(f"Pre-enriched: {len([v for v in pre.values() if v.get('e')])} with meanings")

MAP = {
"nem":"no; not","az":"the; that","hogy":"that; how","es":"and",
"egy":"one; a","van":"is; there is","ez":"this","is":"also; too",
"meg":"and; also","de":"but","csak":"only; just","mi":"what; we",
"ha":"if","en":"I","azt":"that (accusative)","vagy":"or; you are",
"volt":"was; were","igen":"yes","itt":"here","kell":"must; is needed",
"mar":"already","ne":"don't","te":"you (sing.)","meg":"still; yet",
"ki":"who; out","mit":"what (acc.)","jo":"good","most":"now",
"tudom":"I know","ugy":"so; that way","miert":"why",
"mint":"as; like; than","akkor":"then","jol":"well",
"lesz":"will be","nincs":"there isn't","nagyon":"very",
"minden":"every; all","mert":"because","be":"into; in",
"rendben":"alright; ok","le":"down","sem":"neither; nor",
"fel":"up","mas":"other; else","ora":"hour; clock; lesson",
"ember":"person","tud":"knows; can","kicsit":"a little",
"nagy":"big","szeret":"loves; likes","nap":"day; sun",
"tobb":"more","semmi":"nothing","olyan":"such; so",
"utan":"after","helyett":"instead of","nelkul":"without",
"miatt":"because of","ellen":"against","vege":"end",
"eleje":"beginning","darab":"piece","kerdes":"question",
"valasz":"answer","gondolat":"thought","otlet":"idea",
"cel":"goal; aim","penz":"money","munka":"work; job",
"fizetes":"salary","szabadsag":"freedom; vacation",
"reggel":"morning","del":"noon; south","delutan":"afternoon",
"este":"evening","ejszaka":"night",
"hetfo":"Monday","kedd":"Tuesday","szerda":"Wednesday",
"csutortok":"Thursday","pentek":"Friday","szombat":"Saturday",
"vasarnap":"Sunday","het":"week; seven","honap":"month","ev":"year",
"tavasz":"spring","nyar":"summer","osz":"autumn","tel":"winter",
"ido":"time; weather","ma":"today","tegnap":"yesterday",
"holnap":"tomorrow","anya":"mother","apa":"father",
"testver":"sibling","fiu":"boy; son","lany":"girl; daughter",
"gyerek":"child","feleseg":"wife","ferj":"husband",
"barat":"friend","tanar":"teacher","diak":"student",
"orvos":"doctor","rendor":"police officer","katona":"soldier",
"mernok":"engineer","iro":"writer","enekes":"singer",
"fej":"head","arc":"face","szem":"eye","ful":"ear",
"szaj":"mouth","fog":"tooth","nyelv":"tongue; language",
"orr":"nose","nyak":"neck","vall":"shoulder","kar":"arm",
"kez":"hand","ujj":"finger","lab":"leg; foot",
"terd":"knee","hat":"back","has":"stomach",
"sziv":"heart","ver":"blood","csont":"bone","bor":"skin",
"etel":"food","ital":"drink","viz":"water","kenyer":"bread",
"tej":"milk","sajt":"cheese","tojas":"egg","hus":"meat",
"hal":"fish; dies","gyumolcs":"fruit","alma":"apple",
"banan":"banana","narancs":"orange","citrom":"lemon",
"zoldseg":"vegetable","paprika":"bell pepper","kukorica":"corn",
"rizs":"rice","teszta":"pasta","so":"salt","cukor":"sugar",
"olaj":"oil","kave":"coffee","tea":"tea","sor":"beer",
"bor":"wine","lakas":"apartment","haz":"house","szoba":"room",
"konyha":"kitchen","ajto":"door","ablak":"window","fal":"wall",
"lepcso":"stairs","asztal":"table","szek":"chair","agy":"bed",
"tukor":"mirror","lampa":"lamp","taska":"bag","ruha":"clothing",
"cip":"shoe","kalap":"hat","nadrag":"trousers","ing":"shirt",
"kabat":"coat","varos":"city","falu":"village","utca":"street",
"ut":"road; way","hid":"bridge","bolt":"shop","iskola":"school",
"egyetem":"university","korhaz":"hospital","templom":"church",
"muzeum":"museum","allat":"animal","kutya":"dog",
"macska":"cat","madar":"bird","lo":"horse","tehen":"cow",
"nyul":"rabbit","eger":"mouse","farkas":"wolf",
"roka":"fox","medve":"bear","oroszl":"lion",
"tigris":"tiger","elefant":"elephant","fa":"tree","virag":"flower",
"fu":"grass","level":"leaf; letter","gyoker":"root",
"erdo":"forest","kert":"garden","mezo":"field",
"folyo":"river","to":"lake","tenger":"sea","hegy":"mountain",
"domb":"hill","volgy":"valley","felho":"cloud","hold":"moon",
"csillag":"star","fold":"earth; ground","ko":"stone",
"homok":"sand","tuz":"fire","fust":"smoke","levego":"air",
"szel":"wind; edge","eso":"rain","ho":"snow","jeg":"ice",
"kod":"fog","megy":"goes","jon":"comes","ment":"went",
"jott":"came","lat":"sees","hall":"hears","beszel":"speaks",
"mond":"says","ker":"asks; requests","ad":"gives",
"vesz":"buys; takes","eszik":"eats","iszik":"drinks",
"alszik":"sleeps","fut":"runs","uszik":"swims",
"jatszik":"plays","olvas":"reads","ir":"writes",
"tanul":"studies; learns","tanit":"teaches",
"var":"waits; castle","kezd":"begins; starts",
"hoz":"brings","visz":"carries; takes",
"szeep":"beautiful","csunya":"ugly","kicsi":"small",
"gyors":"fast","lassu":"slow","eros":"strong",
"gyenge":"weak","olcso":"cheap","fiatal":"young",
"oreg":"old","magas":"tall; high","alacsony":"short; low",
"hosszu":"long","rovid":"short","nehez":"heavy; difficult",
"konnyu":"light; easy","fontos":"important","hasznos":"useful",
"biztos":"sure; certain","igaz":"true","hamis":"false",
"rossz":"bad","okos":"smart; clever","buta":"stupid",
"bator":"brave","szomoru":"sad","merges":"angry",
"boldog":"happy","faradt":"tired","beteg":"sick",
"egeszseges":"healthy","ehes":"hungry","szomjas":"thirsty",
"egyedul":"alone","egyutt":"together",
"mindig":"always","soha":"never","neha":"sometimes",
"lassan":"slowly","gyorsan":"quickly",
"tal":"maybe","persze":"of course",
"sajnos":"unfortunately",
"majdnem":"almost","elso":"first","masodik":"second",
"harmadik":"third","negyedik":"fourth","otodik":"fifth",
"utolso":"last","mindenki":"everyone","senki":"no one",
"valaki":"someone","sok":"many; much","keves":"few; little",
"tobb":"more","kevesebb":"less",
"kulonbozo":"different",
"tavol":"far","kozel":"near",
"belul":"inside","kivul":"outside","elott":"before; in front",
"mogott":"behind","alatt":"under; during",
"mellett":"next to","folott":"above","kozott":"between",
"no":"woman; grows","ferfi":"man","konyv":"book",
"auto":"car","vonat":"train","repulo":"airplane",
"hajo":"ship","bicikli":"bicycle",
"jegy":"ticket","allomas":"station","terkep":"map",
"csomag":"package","szalloda":"hotel","etterem":"restaurant",
"kavez":"cafe","szallas":"accommodation",
"gyogyszer":"medicine","post":"post",
"szo":"word","szam":"number","szin":"color",
"forma":"shape","vonal":"line","kor":"circle",
"sport":"sport","labda":"ball",
"zene":"music","film":"movie","kep":"picture",
"unnep":"celebration","szokas":"habit",
"magyar":"Hungarian","angol":"English","nemet":"German",
"francia":"French","spanyol":"Spanish","olasz":"Italian",
"beszed":"speech","szot":"dictionary",
"igenyes":"demanding","igenytelen":"undemanding",
}

def make_sound(word):
    s = word.lower()
    subs = {"a":"a","e":"e","i":"ee","o":"o","u":"oo",
            "cs":"ch","gy":"dy","ly":"y","ny":"ny",
            "sz":"s","ty":"ty","zs":"zh"}
    for hu, en in sorted(subs.items(), key=lambda x: -len(x[0])):
        s = s.replace(hu, en)
    return s

def make_mnemonic(word, meaning):
    sound = make_sound(word)
    short = meaning.split(";")[0].split(",")[0][:50]
    return f'Spoken like "{sound}" — {short}.'

entries = []
preserved, mapped, fallback = 0, 0, 0

for word in csv_words:
    if not word:
        continue
    if word in pre and pre[word].get("e"):
        entries.append(pre[word])
        preserved += 1
        continue
    w_lower = word.lower()
    found = False
    for key in MAP:
        if w_lower == key.lower() or w_lower.startswith(key.lower()):
            meaning = MAP[key]
            mnemonic = make_mnemonic(word, meaning)
            entries.append({"h": word, "e": meaning, "m": mnemonic})
            mapped += 1
            found = True
            break
    if not found:
        fallback += 1
        sound = make_sound(word)
        entries.append({"h": word, "e": "(Hungarian word)", "m": f'Spoken like "{sound}".'})

print(f"\nPreserved: {preserved}")
print(f"Mapped: {mapped}")
print(f"Fallback: {fallback}")
print(f"Total: {len(entries)}")

os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "words.js")
with open(path, "w", encoding="utf-8") as f:
    f.write("// Hungarian-English vocabulary database\n")
    f.write(f"// {len(entries)} words from 5K.csv\n")
    f.write("const wordDatabase = ")
    f.write(json.dumps(entries, ensure_ascii=False, indent=2))
    f.write(";\n")

size = os.path.getsize(path)
print(f"\nWritten to: {path}")
print(f"Size: {size:,} bytes ({size/1024:.0f} KB)")
