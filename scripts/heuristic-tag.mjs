// Heuristic POS + theme tagger for Hungarian vocabulary entries.
// Tags clear-cut cases. Leaves uncertain entries untagged for later LLM refinement.
// Usage: node scripts/heuristic-tag.mjs [--dry-run]
//
// This covers ~60-70% of entries with high confidence. Remaining entries
// need human review or LLM tagging (scripts/tag-words.mjs).

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const WORDS_PATH = path.join(ROOT, "lib", "words.js");
const BACKUP_PATH = path.join(ROOT, "lib", "words.backup.heuristic.js");

const DRY_RUN = process.argv.includes("--dry-run");

// ---- Load word database -------------------------------------------------
console.log(`Reading ${WORDS_PATH} ...`);
const source = fs.readFileSync(WORDS_PATH, "utf-8");
const fnBody = source.replace("export const wordDatabase =", "return");
const wordDatabase = new Function(fnBody)();
console.log(`Loaded ${wordDatabase.length} entries.\n`);

// ---- Known Hungarian closed-class words ---------------------------------
// These are hand-curated sets of known Hungarian function words, verb
// prefixes, pronouns, and numbers. Adding words here is safe.

// Function words: articles, conjunctions, postpositions, particles
const FUNC_WORDS = new Set([
  // Articles
  "a", "az", "egy",
  // Conjunctions
  "és", "de", "hogy", "mert", "vagy", "ha", "mint", "pedig",
  "tehát", "viszont", "azonban", "bár", "hiszen", "mintha",
  "ám", "ellenben", "meg", "s", "sőt", "valamint",
  // Postpositions
  "alatt", "alá", "alól", "által", "előtt", "elé", "elől",
  "felett", "fölé", "felől", "mellett", "mellé", "mellől",
  "mögött", "mögé", "mögül", "között", "közé", "közül",
  "után", "ellen", "helyett", "iránt", "körül", "miatt",
  "nélkül", "óta", "szerint", "szemben", "túl", "át",
  "belül", "kívül", "felül", "alul", "keresztül",
  // Particles / discourse markers
  "is", "sem", "se", "nem", "ne", "csak", "már", "még",
  "igen", "persze", "vajon", "ugye", "hát", "nos", "szívesen",
  // Question words (interrogative particles — could be pron, but function role)
  "-e",
  // Case suffixes that appear as standalone entries
  "-ban", "-ben", "-ba", "-be", "-ra", "-re", "-ról", "-ről",
  "-tól", "-től", "-hoz", "-hez", "-höz", "-nál", "-nél",
  "-val", "-vel", "-ért", "-ig", "-nak", "-nek", "-on", "-en", "-ön",
  "-ul", "-ül", "-ként", "-kor", "-szor", "-szer", "-ször",
]);

// Verb prefixes (igekötők) — closed set
const PREF_WORDS = new Set([
  "meg", "el", "ki", "be", "fel", "le", "át", "rá", "ide", "oda",
  "össze", "szét", "vissza", "haza", "végig", "körül", "hozzá",
  "bele", "benn", "fenn", "lenn", "kinn", "túl", "utána",
  "egybe", "szembe", "agyon", "alább", "félbe", "félre",
  "hátra", "helyre", "jóvá", "ketté", "közre", "külön",
  "újjá", "útra", "végbe", "véghez", "viszont",
]);

// Hungarian personal / demonstrative / interrogative pronouns
const PRON_WORDS = new Set([
  // Personal
  "én", "te", "ő", "mi", "ti", "ők",
  // Accusative / oblique personal forms that appear as headwords
  "engem", "téged", "őt", "minket", "titeket", "őket",
  "nekem", "neked", "neki", "nekünk", "nektek", "nekik",
  // Dative / other cased forms (common headwords)
  "rólam", "rólad", "róla", "rólunk", "rólatok", "róluk",
  "tőlem", "tőled", "tőle", "tőlünk", "tőletek", "tőlük",
  "hozzám", "hozzád", "hozzá", "hozzánk", "hozzátok", "hozzájuk",
  "nálam", "nálad", "nála", "nálunk", "nálatok", "náluk",
  "bennem", "benned", "benne", "bennünk", "bennetek", "bennük",
  "belém", "beléd", "belé", "belénk", "belétek", "beléjük",
  "rajtam", "rajtad", "rajta", "rajtunk", "rajtatok", "rajtuk",
  "rám", "rád", "rá", "ránk", "rátok", "rájuk",
  // Demonstrative
  "ez", "az", "ezek", "azok", "ilyen", "olyan", "ennyi", "annyi",
  "ekkora", "akkora", "ilyenkor", "itt", "ott", "ide", "oda",
  "innen", "onnan", "így", "úgy",
  // Interrogative / relative
  "ki", "mi", "melyik", "milyen", "mekkora", "mennyi", "hány",
  "hol", "hova", "honnan", "mikor", "miért", "meddig",
  // Reflexive / reciprocal
  "maga", "magam", "magad", "magát", "magunk", "magatok", "maguk",
  "egymás",
  // General / indefinite pronouns
  "valaki", "valami", "mindenki", "minden", "senki", "semmi",
  "bárki", "bármi", "néhány", "valamilyen", "némelyik",
]);

// ---- Theme mapping from English keywords --------------------------------
function inferThemes(english) {
  if (!english) return [];
  const lower = english.toLowerCase();
  const themes = [];

  const rules = [
    [/\b(father|mother|brother|sister|son|daughter|uncle|aunt|cousin|parent|child|family|husband|wife|friend|boy|girl|man|woman|men|women|person|people|baby|king|queen|mister|miss|sir|lady|lord|mr\.?|mrs\.?|neighbor|neighbour)\b/, "people"],
    [/\b(eat|drink|cook|bake|food|bread|meat|water|wine|beer|milk|coffee|tea|soup|salt|sugar|apple|fruit|vegetable|rice|egg|cheese|butter|oil|flour|meal|breakfast|lunch|dinner|hungry|thirsty|taste|kitchen|plate|cup|glass|bottle)\b/, "food"],
    [/\b(time|day|night|week|month|year|today|tomorrow|yesterday|morning|evening|afternoon|hour|minute|second|moment|always|never|sometimes|often|soon|later|early|late|now|then|when|while|during|already|still|yet|clock|season|spring|summer|autumn|winter|january|february|march|april|may|june|july|august|september|october|november|december|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b/, "time"],
    [/\b(here|there|where|place|room|house|home|street|road|city|town|country|village|world|building|door|window|wall|floor|garden|yard|square|space|direction|left|right|up|down|front|back|side|top|bottom|inside|outside|between|among|near|far|above|below|under|over|next|opposite|behind|ahead|around|through|across|along|towards?|away)\b/, "space"],
    [/\b(one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|million|first|second|third|number|count|many|few|much|little|more|less|half|whole|all|some|several|enough|each|every|both|most|least|none|pair|couple|dozen|percent|double|triple)\b/, "quantity"],
    [/\b(big|small|large|tiny|tall|short|long|wide|narrow|thick|thin|heavy|light|hard|soft|hot|cold|warm|cool|fast|slow|quick|old|new|young|good|bad|nice|beautiful|ugly|pretty|rich|poor|clean|dirty|wet|dry|full|empty|deep|shallow|strong|weak|bright|dark|color|red|blue|green|yellow|white|black|brown|grey|gray|pink|purple|orange)\b/, "quality"],
    [/\b(run|walk|go|come|bring|take|carry|put|set|stand|sit|lie|fall|rise|move|turn|push|pull|throw|catch|hit|break|cut|open|close|start|stop|begin|finish|build|make|do|work|use|give|get|receive|send|hold|keep|let|leave|enter|arrive|depart|pass|cross|jump|climb|fly|swim|drive|ride|travel)\b/, "action"],
    [/\b(think|know|believe|feel|want|need|like|love|hate|hope|wish|fear|remember|forget|understand|learn|teach|study|read|write|speak|say|tell|ask|answer|call|cry|laugh|smile|sleep|wake|dream|live|die|hurt|suffer|enjoy|care|mind|mean|seem|appear|become|happen|change|stay)\b/, "state"],
    [/\b(water|fire|air|earth|sky|sun|moon|star|rain|snow|wind|cloud|storm|river|lake|sea|ocean|mountain|hill|forest|tree|flower|grass|leaf|stone|rock|sand|gold|silver|iron|wood|metal|animal|dog|cat|horse|cow|pig|sheep|bird|fish|snake|insect|bear|wolf|fox|deer)\b/, "nature"],
    [/\b(head|hand|foot|eye|ear|nose|mouth|tooth|tongue|face|hair|neck|back|arm|leg|finger|heart|blood|bone|skin|body|stomach|liver|brain)\b/, "body"],
    [/\b(say|speak|talk|tell|ask|answer|word|language|speech|voice|sound|call|shout|whisper|noise|quiet|loud|write|read|letter|book|paper|news|story|question|name|meaning|sign)\b/, "communication"],
    [/\b(think|idea|mind|reason|logic|true|false|real|fact|problem|solution|cause|effect|result|way|method|kind|type|part|thing|something|nothing|everything|same|different|other|possible|necessary|important|special|general|certain|maybe|perhaps|probably|sure|maybe|if|then|because|why|how|what|when|where|who)\b/, "abstract"],
    [/\b(the|a|an|and|or|but|not|to|of|in|on|at|by|for|with|from|as|than|that|this|it|is|are|was|were|be|been|has|have|had|do|does|did|will|would|can|could|shall|should|may|might|must|so|very|too|also|just|only|even|still|yet|already|always|never|here|there|now|then|well|please|yes|no)\b/, "function"],
  ];

  for (const [regex, theme] of rules) {
    if (regex.test(lower)) {
      themes.push(theme);
    }
  }

  // Deduplicate
  return [...new Set(themes)];
}

// ---- Main tagging logic -------------------------------------------------
function tagEntry(w) {
  const h = w.h || "";
  const e = (w.e || "").toLowerCase();

  // 1. Known function words (highest priority — override other heuristics)
  if (FUNC_WORDS.has(h)) {
    return { p: "func", t: ["function"] };
  }

  // 2. Verb prefixes
  if (PREF_WORDS.has(h)) {
    return { p: "pref", t: [] };
  }

  // 3. Known pronouns
  if (PRON_WORDS.has(h)) {
    return { p: "pron", t: ["people"] };
  }

  // 4. Numbers from English text
  if (/^(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|zero|half|dozen|[0-9]+)(st|nd|rd|th)?$/i.test(e.trim())) {
    return { p: "num", t: ["quantity"] };
  }

  // 5. Interjections from English
  if (/^[a-záéíóöőúüű]+!$/i.test(h) || /\b(hey|hi|hello|bye|wow|oh|ah|uh|hm|alas|bravo|hurrah|ouch|oops|yay|yikes)\b/i.test(e)) {
    return { p: "interj", t: [] };
  }

  // 6. Adverbs from English parenthetical
  if (/\(adverb\)/i.test(e) || /\b(adverb)\b/i.test(e)) {
    return { p: "adv", t: inferThemes(e) };
  }

  // 7. Adjectives from English parenthetical
  if (/\(adjective\)/i.test(e) || /\b(adjective)\b/i.test(e)) {
    return { p: "adj", t: inferThemes(e) };
  }

  // 8. Pronouns from English parenthetical
  if (/\(pronoun\)/i.test(e) || /\b(pronoun)\b/i.test(e)) {
    return { p: "pron", t: ["people"] };
  }

  // 9. Conjunctions from English parenthetical
  if (/\(conjunction\)/i.test(e)) {
    return { p: "func", t: ["function"] };
  }

  // 10. Verb prefixes from English text
  if (/\b(verbal prefix|coverb|preverb)\b/i.test(e)) {
    return { p: "pref", t: [] };
  }

  // 11. For the remaining "to X" patterns: if the English is just "to X"
  // and X isn't a Hungarian pronoun, treat as verb
  // But this is unreliable — skip for now, let LLM handle

  // 12. If English explicitly states "(Hungarian word)" or is empty
  if (!e || e === "(hungarian word)") {
    return { p: undefined, t: [] }; // Leave POS untagged
  }

  // Default: infer themes but leave POS untagged
  return { p: undefined, t: inferThemes(e) };
}

// ---- Apply tags ---------------------------------------------------------
let posTagged = 0;
let themeTagged = 0;
let bothTagged = 0;
let untagged = 0;

for (const w of wordDatabase) {
  // Skip already-tagged entries (from previous LLM runs)
  if (w.p && w.t) continue;

  const { p, t } = tagEntry(w);

  if (p) {
    w.p = p;
    posTagged++;
  }
  if (t && t.length > 0) {
    // Merge with existing themes if any, deduplicate
    const existing = w.t || [];
    w.t = [...new Set([...existing, ...t])];
    themeTagged++;
  }
  if (p && t && t.length > 0) bothTagged++;
  if (!p && (!t || t.length === 0)) untagged++;
}

console.log(`Results:`);
console.log(`  POS tagged:     ${posTagged}/${wordDatabase.length}`);
console.log(`  Theme tagged:   ${themeTagged}/${wordDatabase.length}`);
console.log(`  Both tagged:    ${bothTagged}/${wordDatabase.length}`);
console.log(`  Still untagged: ${untagged}/${wordDatabase.length}`);

// POS distribution
const posCounts = {};
for (const w of wordDatabase) {
  const key = w.p || "untagged";
  posCounts[key] = (posCounts[key] || 0) + 1;
}
console.log("\nPOS distribution:");
for (const [k, v] of Object.entries(posCounts).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${k}: ${v}`);
}

// Theme distribution
const themeCounts = {};
for (const w of wordDatabase) {
  if (w.t) {
    for (const t of w.t) {
      themeCounts[t] = (themeCounts[t] || 0) + 1;
    }
  }
}
console.log("\nTheme distribution:");
for (const [k, v] of Object.entries(themeCounts).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${k}: ${v}`);
}

// ---- Write output -------------------------------------------------------
function serializeEntry(w, indent) {
  const fields = [];
  fields.push(`${indent}  "h": ${JSON.stringify(w.h)}`);
  fields.push(`${indent}  "e": ${JSON.stringify(w.e)}`);
  fields.push(`${indent}  "m": ${JSON.stringify(w.m)}`);
  fields.push(`${indent}  "i": ${JSON.stringify(w.i)}`);
  if (w.p) fields.push(`${indent}  "p": ${JSON.stringify(w.p)}`);
  if (w.t && w.t.length) fields.push(`${indent}  "t": ${JSON.stringify(w.t)}`);
  return `${indent}{\n${fields.join(",\n")}\n${indent}}`;
}

if (!DRY_RUN) {
  // Backup
  if (!fs.existsSync(BACKUP_PATH)) {
    fs.copyFileSync(WORDS_PATH, BACKUP_PATH);
    console.log(`\nBacked up to ${BACKUP_PATH}`);
  }

  const lines = [];
  lines.push("// Hungarian-English vocabulary database");
  lines.push("// 4550 words from 5K.csv");
  lines.push("/* ponytail: POS/theme tags added as optional fields — no separate lookup table (YAGNI) */");
  lines.push("export const wordDatabase = [");

  wordDatabase.forEach((w, i) => {
    const comma = i < wordDatabase.length - 1 ? "," : "";
    lines.push(serializeEntry(w, "  ") + comma);
  });

  lines.push("];");
  lines.push("");

  fs.writeFileSync(WORDS_PATH, lines.join("\n"), "utf-8");
  console.log(`Wrote ${WORDS_PATH}`);
} else {
  console.log("\n(Dry run — no files written.)");
}

// Show a sample of tagged entries
console.log("\nSample tagged entries:");
const tagged = wordDatabase.filter((w) => w.p && w.t && w.t.length);
for (let i = 0; i < Math.min(15, tagged.length); i++) {
  const w = tagged[Math.floor(Math.random() * tagged.length)];
  console.log(`  ${w.h} → POS:${w.p}  theme:${(w.t || []).join(",")}  (${w.e})`);
}

console.log("\nSample untagged entries:");
const untaggedList = wordDatabase.filter((w) => !w.p || !w.t || !w.t.length);
for (let i = 0; i < Math.min(10, untaggedList.length); i++) {
  const w = untaggedList[Math.floor(Math.random() * untaggedList.length)];
  console.log(`  ${w.h} → (${w.e})`);
}
