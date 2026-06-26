#!/usr/bin/env python3
"""Generate Hungarian-English vocabulary database from 5K.csv + vocab.js"""

import json, re, os, random

DATA = "C:/Users/admin/Desktop/design_handoff_hungarian_vocab/data"
OUT = "C:/Users/admin/Desktop/vocab-app"

# Load CSV words
with open(os.path.join(DATA, "5K.csv"), "r", encoding="utf-8") as f:
    csv_words = [l.strip() for l in f if l.strip()]
print(f"5K.csv: {len(csv_words)} words")

# Load pre-enriched entries using regex (vocab.js uses JS object syntax, not JSON)
with open(os.path.join(DATA, "vocab.js"), "r", encoding="utf-8") as f:
    js = f.read()
pre = {}
# Match {h:"...", e:"...", m:"..."} patterns
for m in re.finditer(r'\{h:"([^"]*)",\s*e:"([^"]*)",\s*m:"([^"]*)"\}', js):
    h, e, mn = m.group(1), m.group(2), m.group(3)
    pre[h] = {"h": h, "e": e, "m": mn}
# Also match {h:"..."} without e/m
for m in re.finditer(r'\{h:"([^"]*)"\}', js):
    h = m.group(1)
    if h not in pre:
        pre[h] = {"h": h}
print(f"Pre-enriched entries with meanings: {len([v for v in pre.values() if v.get('e')])}")
print(f"Total entries in vocab.js: {len(pre)}")

# Hungarian-English word map (concise glosses)
MAP = {
"nem":"no; not","az":"the (before vowels); that","hogy":"that; how","és":"and",
"egy":"one; a/an","van":"is; there is","ez":"this","is":"also; too",
"meg":"and; also","de":"but","csak":"only; just","mi":"what; we","ha":"if",
"én":"I","azt":"that (accusative)","vagy":"or; you are","volt":"was; were",
"igen":"yes","itt":"here","kell":"must; is needed","el":"away; off",
"már":"already","ne":"don't","te":"you (singular)","még":"still; yet",
"ki":"who; out","mit":"what (accusative)","jó":"good","vagyok":"I am",
"ezt":"this (accusative)","most":"now","tudom":"I know","úgy":"so; that way",
"miért":"why","mint":"as; like; than","akkor":"then","jól":"well",
"lesz":"will be","nincs":"there isn't","nagyon":"very",
"minden":"every; all","mert":"because","be":"into; in",
"rendben":"alright; okay","le":"down","sem":"neither; nor",
"amit":"what (relative)","fel":"up","más":"other; else","aki":"who (relative)",
"óra":"hour; clock; lesson","ember":"person; human","tud":"knows; can",
"kicsit":"a little","nagy":"big; large","szeret":"loves; likes",
"emberek":"people","ilyen":"such; like this","nap":"day; sun",
"több":"more","kellene":"should; would need","semmi":"nothing",
"olyan":"such; so","amikor":"when","után":"after; behind",
"helyett":"instead of","nélkül":"without","óta":"since",
"miatt":"because of","ellen":"against","szerint":"according to",
"vége":"end","eleje":"beginning","darab":"piece; item",
"dolog":"thing; matter","kérdés":"question","válasz":"answer",
"gondolat":"thought","ötlet":"idea","tény":"fact","ok":"cause; reason",
"cél":"goal; aim","hatás":"effect","jelentés":"meaning; report",
"érték":"value","ár":"price","pénz":"money","munka":"work; job",
"fizetés":"salary; payment","szabadság":"freedom; vacation",
"szünet":"break; pause","reggel":"morning","dél":"noon; south",
"délután":"afternoon","este":"evening","éjszaka":"night",
"hétfő":"Monday","kedd":"Tuesday","szerda":"Wednesday",
"csütörtök":"Thursday","péntek":"Friday","szombat":"Saturday",
"vasárnap":"Sunday","hét":"week; seven","hónap":"month","év":"year",
"tavasz":"spring","nyár":"summer","ősz":"autumn; fall","tél":"winter",
"idő":"time; weather","ma":"today","tegnap":"yesterday","holnap":"tomorrow",
"anya":"mother","apa":"father","testvér":"sibling","fiú":"boy; son",
"lány":"girl; daughter","gyerek":"child","feleség":"wife","férj":"husband",
"barát":"friend","tanár":"teacher","diák":"student","orvos":"doctor",
"rendőr":"police officer","katona":"soldier","szakács":"cook; chef",
"mérnök":"engineer","festő":"painter","író":"writer","zenész":"musician",
"énekes":"singer","színész":"actor",
"fej":"head","arc":"face","szem":"eye","fül":"ear","száj":"mouth",
"fog":"tooth; catches","nyelv":"tongue; language","orr":"nose",
"nyak":"neck","váll":"shoulder","kar":"arm","kéz":"hand","ujj":"finger",
"láb":"leg; foot","térd":"knee","hát":"back","has":"stomach; belly",
"szív":"heart","vér":"blood","csont":"bone","bőr":"skin","haj":"hair",
"étel":"food","ital":"drink","víz":"water","kenyér":"bread","tej":"milk",
"sajt":"cheese","tojás":"egg","hús":"meat","hal":"fish; dies",
"csirke":"chicken","gyümölcs":"fruit","alma":"apple","körte":"pear",
"banán":"banana","narancs":"orange","citrom":"lemon","szőlő":"grape",
"zöldség":"vegetable","paradicsom":"tomato","uborka":"cucumber",
"répa":"carrot","hagyma":"onion","fokhagyma":"garlic",
"káposzta":"cabbage","paprika":"bell pepper","kukorica":"corn",
"rizs":"rice","tészta":"pasta; dough","só":"salt","cukor":"sugar",
"liszt":"flour","olaj":"oil","kávé":"coffee","tea":"tea","sör":"beer",
"bor":"wine","lakás":"apartment","ház":"house","szoba":"room",
"konyha":"kitchen","ajtó":"door","ablak":"window","fal":"wall",
"tető":"roof","emelet":"floor; story","lépcső":"stairs",
"bútor":"furniture","asztal":"table","szék":"chair","ágy":"bed",
"szekrény":"wardrobe","tükör":"mirror","lámpa":"lamp",
"táska":"bag","ruha":"clothing","cipő":"shoe","kalap":"hat",
"nadrág":"trousers","ing":"shirt","kabát":"coat",
"város":"city","falu":"village","utca":"street","út":"road; way",
"tér":"square","híd":"bridge","bolt":"shop","iskola":"school",
"egyetem":"university","kórház":"hospital","templom":"church",
"múzeum":"museum","park":"park",
"állat":"animal","kutya":"dog","macska":"cat","madár":"bird",
"ló":"horse","tehén":"cow","nyúl":"rabbit","egér":"mouse",
"farkas":"wolf","róka":"fox","medve":"bear","oroszlán":"lion",
"tigris":"tiger","elefánt":"elephant",
"fa":"tree","virág":"flower","fű":"grass","levél":"leaf; letter",
"gyökér":"root","mag":"seed","ág":"branch","erdő":"forest",
"kert":"garden","mező":"field",
"folyó":"river","tó":"lake","tenger":"sea","hegy":"mountain",
"domb":"hill","völgy":"valley","ég":"sky","felhő":"cloud",
"hold":"moon","csillag":"star","föld":"earth; ground","kő":"stone",
"homok":"sand","tűz":"fire","füst":"smoke","levegő":"air",
"szél":"wind; edge","eső":"rain","hó":"snow","jég":"ice","köd":"fog",
"megy":"goes","jön":"comes","ment":"went","jött":"came",
"csinál":"does; makes","lát":"sees","hall":"hears","beszél":"speaks",
"mond":"says","kér":"asks; requests","ad":"gives","vesz":"buys; takes",
"eszik":"eats","iszik":"drinks","alszik":"sleeps","fut":"runs",
"úszik":"swims","játszik":"plays","olvas":"reads","ír":"writes",
"tanul":"studies; learns","tanít":"teaches",
"vár":"waits; castle","kezd":"begins; starts","hoz":"brings",
"visz":"carries; takes","szép":"beautiful","csúnya":"ugly",
"kicsi":"small","gyors":"fast","lassú":"slow","erős":"strong",
"gyenge":"weak","drága":"expensive","olcsó":"cheap",
"fiatal":"young","öreg":"old","magas":"tall; high",
"alacsony":"short; low","hosszú":"long","rövid":"short",
"nehéz":"heavy; difficult","könnyű":"light; easy","fontos":"important",
"hasznos":"useful","biztos":"sure; certain","igaz":"true",
"hamis":"false","rossz":"bad","kedves":"kind; dear",
"gonosz":"evil; mean","okos":"smart; clever","buta":"stupid",
"bátor":"brave","vidám":"cheerful","szomorú":"sad","mérges":"angry",
"boldog":"happy","fáradt":"tired","beteg":"sick",
"egészséges":"healthy","éhes":"hungry","szomjas":"thirsty",
"egyedül":"alone","együtt":"together",
"mindig":"always","soha":"never","gyakran":"often","ritkán":"rarely",
"néha":"sometimes","lassan":"slowly","gyorsan":"quickly",
"talán":"maybe; perhaps","persze":"of course",
"sajnos":"unfortunately","szerencsére":"fortunately",
"körülbelül":"approximately","majdnem":"almost; nearly",
"például":"for example","első":"first","második":"second",
"harmadik":"third","negyedik":"fourth","ötödik":"fifth",
"utolsó":"last","mindenki":"everyone","senki":"no one",
"valaki":"someone","sok":"many; much","kevés":"few; little",
"rengeteg":"a lot; plenty","különböző":"different; various",
"hasonló":"similar","távol":"far","közel":"near",
"belül":"inside","kívül":"outside","előtt":"before; in front of",
"mögött":"behind","alatt":"under; during","mellett":"next to; beside",
"fölött":"above","között":"between; among",
"nő":"woman; grows","férfi":"man","gyerek":"child",
"könyv":"book","autó":"car","vonat":"train",
"r
