// Batch-tag Hungarian vocabulary entries with POS and theme using an LLM.
// Usage: node scripts/tag-words.mjs [--dry-run] [--start N] [--end N] [--batch-size N]
//
// Reads lib/words.js, sends batches to the OpenAI-compatible API configured
// via OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL env vars (same as the
// Translator feature), then writes back lib/words.js with added "p" and "t"
// fields.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const WORDS_PATH = path.join(ROOT, "lib", "words.js");
const BACKUP_PATH = path.join(ROOT, "lib", "words.backup.js");
const PROGRESS_PATH = path.join(ROOT, "lib", "words.progress.json");

// ---- CLI args -----------------------------------------------------------
const args = process.argv.slice(2);
const DRY_RUN = args.includes("--dry-run");
const START = parseInt(args[args.indexOf("--start") + 1] || "0", 10);
const END = parseInt(args[args.indexOf("--end") + 1] || "0", 10) || Infinity;
const BATCH_SIZE = parseInt(args[args.indexOf("--batch-size") + 1] || "50", 10);

// ---- API config ---------------------------------------------------------
const API_KEY = process.env.OPENAI_API_KEY;
const BASE_URL = (process.env.OPENAI_BASE_URL || "https://api.openai.com").replace(/\/+$/, "");
const MODEL = process.env.OPENAI_MODEL || "gpt-3.5-turbo";

if (!API_KEY) {
  console.error("ERROR: OPENAI_API_KEY not set.");
  console.error("Create a .env file at the project root with:");
  console.error("  OPENAI_API_KEY=your_key_here");
  console.error("  OPENAI_BASE_URL=https://api.openai.com/v1  (optional)");
  console.error("  OPENAI_MODEL=gpt-3.5-turbo                   (optional)");
  process.exit(1);
}

// ---- Load word database -------------------------------------------------
console.log(`Reading ${WORDS_PATH} ...`);
const source = fs.readFileSync(WORDS_PATH, "utf-8");
// Transform "export const wordDatabase = [...]" into "return [...]"
const fnBody = source.replace("export const wordDatabase =", "return");
const wordDatabase = new Function(fnBody)();
console.log(`Loaded ${wordDatabase.length} entries.`);
console.log(`API: ${BASE_URL}  model: ${MODEL}`);
console.log(`Range: ${START} – ${END === Infinity ? wordDatabase.length : END}`);
console.log(`Batch size: ${BATCH_SIZE}  Dry run: ${DRY_RUN}\n`);

// ---- Load progress (for resume) -----------------------------------------
let doneIndices = new Set();
if (fs.existsSync(PROGRESS_PATH)) {
  doneIndices = new Set(JSON.parse(fs.readFileSync(PROGRESS_PATH, "utf-8")));
  console.log(`Resuming — ${doneIndices.size} entries already tagged.\n`);
}

// ---- Prompt --------------------------------------------------------------
function buildTagPrompt(batch) {
  const entries = batch
    .map(
      (w, i) =>
        `${i + 1}. Hungarian: "${w.h}"  English: "${w.e || ""}"  IPA: "${w.i || ""}"`
    )
    .join("\n");

  return [
    {
      role: "system",
      content: `You tag Hungarian vocabulary entries for a language-learning app.

For each entry, return:
- "i": the 1-based index from the input list
- "p": ONE part-of-speech tag from this closed set:
    n       noun (főnév)
    v       verb (ige)
    adj     adjective (melléknév)
    adv     adverb (határozószó)
    pron    pronoun (névmás)
    func    function word — articles, conjunctions, postpositions, particles
    num     numeral (számnév)
    interj  interjection (indulatszó)
    pref    verbal prefix / coverb (igekötő) — e.g., meg, el, ki, be, fel, le
- "t": ONE OR MORE theme tags from this closed set (array of strings):
    people, action, state, time, space, quantity, quality, nature,
    food, body, abstract, communication, function

Rules:
- "func" covers: articles (a/az, egy), conjunctions (és, de, hogy, mint),
  postpositions (alatt, előtt), and particles (is, sem, -e).
- "pref" covers Hungarian verbal prefixes (igekötők) like meg, el, ki, be,
  fel, le, át, rá, össze, szét, vissza, oda, haza, etc. — even when they
  sometimes appear as standalone adverbs.
- "pron" includes personal (én, te, ő), demonstrative (ez, az), interrogative
  (ki, mi), and possessive pronouns.
- If a word can be multiple POS (e.g., "reggel" = noun "morning" AND adverb
  "in the morning"), pick the MOST COMMON usage.
- For "t", assign the most relevant theme(s). Omit "t" entirely (empty
  array) if nothing fits rather than forcing a bad tag.
- IPA uses // delimiters; the IPA content may help disambiguate.

Return ONLY a JSON array:
[{"i":1,"p":"n","t":["time"]},{"i":2,"p":"v","t":["action","communication"]},...]

No markdown, no extra text.`,
    },
    {
      role: "user",
      content: `Tag these ${batch.length} Hungarian words:\n\n${entries}`,
    },
  ];
}

// ---- API call ------------------------------------------------------------
async function tagBatch(batch) {
  const messages = buildTagPrompt(batch);

  const res = await fetch(`${BASE_URL}/v1/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      model: MODEL,
      messages,
      temperature: 0.3,
      max_tokens: 2048,
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`API ${res.status}: ${err.slice(0, 200)}`);
  }

  const data = await res.json();
  const content = data.choices?.[0]?.message?.content?.trim() || "";

  // Parse JSON — strip possible markdown fences
  const clean = content.replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/i, "");
  try {
    return JSON.parse(clean);
  } catch {
    // Try to find a JSON array anywhere in the response
    const m = clean.match(/\[[\s\S]*\]/);
    if (m) return JSON.parse(m[0]);
    throw new Error(`Could not parse response: ${clean.slice(0, 200)}`);
  }
}

// ---- Write-back helpers --------------------------------------------------
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

function writeDatabase() {
  const lines = [];
  lines.push("// Hungarian-English vocabulary database");
  lines.push("// 4550 words from 5K.csv");
  lines.push("// POS/theme tags added via LLM batch processing (scripts/tag-words.mjs)");
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
}

function saveProgress() {
  fs.writeFileSync(
    PROGRESS_PATH,
    JSON.stringify([...doneIndices]),
    "utf-8"
  );
}

// ---- Main loop -----------------------------------------------------------
async function main() {
  // Back up original
  if (!DRY_RUN && !fs.existsSync(BACKUP_PATH)) {
    fs.copyFileSync(WORDS_PATH, BACKUP_PATH);
    console.log(`Backed up to ${BACKUP_PATH}\n`);
  }

  const endIdx = Math.min(END, wordDatabase.length);
  const toProcess = [];
  for (let i = START; i < endIdx; i++) {
    if (!doneIndices.has(i)) toProcess.push(i);
  }

  if (toProcess.length === 0) {
    console.log("All entries already tagged. Nothing to do.");
    return;
  }

  console.log(`${toProcess.length} entries to process.\n`);

  let batchNum = 0;
  for (let offset = 0; offset < toProcess.length; offset += BATCH_SIZE) {
    batchNum++;
    const indices = toProcess.slice(offset, offset + BATCH_SIZE);
    const batch = indices.map((i) => ({ ...wordDatabase[i], _idx: i }));

    console.log(
      `Batch ${batchNum}  [${indices[0] + 1}–${indices[indices.length - 1] + 1}]  (${indices.length} words) ...`
    );

    let tags;
    try {
      tags = await tagBatch(batch);
    } catch (err) {
      console.error(`  ERROR: ${err.message}`);
      console.error("  Saving progress and aborting. Re-run to resume.");
      saveProgress();
      process.exit(1);
    }

    if (!Array.isArray(tags)) {
      console.error(`  ERROR: Expected array, got ${typeof tags}`);
      saveProgress();
      process.exit(1);
    }

    let applied = 0;
    for (const tag of tags) {
      const batchIdx = tag.i - 1; // 1-based → 0-based within batch
      if (batchIdx < 0 || batchIdx >= batch.length) {
        console.warn(`  WARN: index ${tag.i} out of range (batch size ${batch.length}), skipping`);
        continue;
      }
      const globalIdx = batch[batchIdx]._idx;
      if (tag.p) wordDatabase[globalIdx].p = tag.p;
      if (tag.t && Array.isArray(tag.t) && tag.t.length) {
        wordDatabase[globalIdx].t = tag.t;
      }
      doneIndices.add(globalIdx);
      applied++;
    }

    console.log(`  ✓ Tagged ${applied}/${batch.length} entries`);

    if (!DRY_RUN) {
      writeDatabase();
      saveProgress();
    }

    // Small pause between batches to be polite to the API
    if (offset + BATCH_SIZE < toProcess.length) {
      await new Promise((r) => setTimeout(r, 500));
    }
  }

  console.log(`\nDone! ${doneIndices.size}/${wordDatabase.length} entries tagged.`);

  if (DRY_RUN) {
    console.log("(Dry run — no files were written.)");
  } else {
    // Clean up progress file on success
    if (fs.existsSync(PROGRESS_PATH)) fs.unlinkSync(PROGRESS_PATH);
    // Show stats
    const counts = {};
    for (const w of wordDatabase) {
      counts[w.p || "untagged"] = (counts[w.p || "untagged"] || 0) + 1;
    }
    console.log("\nPOS distribution:");
    for (const [k, v] of Object.entries(counts).sort((a, b) => b[1] - a[1])) {
      console.log(`  ${k}: ${v}`);
    }
  }
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
