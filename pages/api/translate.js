import { wordDatabase } from "@/lib/words";

const MAX_INPUT_LENGTH = 500;
const MAX_DICTIONARY_ENTRIES = 40;

function detectLanguage(text) {
  const lower = text.toLowerCase();
  // Hungarian-specific characters
  if (/[áéíóöőúüű]/u.test(lower)) return "hu";
  // Vietnamese-specific characters
  if (/[àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]/u.test(lower)) return "vi";
  // Default to English
  return "en";
}

function buildPrompt(text, direction, dictionary) {
  let sourceLang, targetLang;
  if (direction === "en2hu") {
    sourceLang = "English";
    targetLang = "Hungarian";
  } else if (direction === "hu2en") {
    sourceLang = "Hungarian";
    targetLang = "English";
  } else if (direction === "vi2hu") {
    sourceLang = "Vietnamese";
    targetLang = "Hungarian";
  } else {
    const detected = detectLanguage(text);
    if (detected === "hu") {
      sourceLang = "Hungarian";
      targetLang = "English";
    } else if (detected === "vi") {
      sourceLang = "Vietnamese";
      targetLang = "Hungarian";
    } else {
      sourceLang = "English";
      targetLang = "Hungarian";
    }
  }

  const dictText = dictionary
    .slice(0, MAX_DICTIONARY_ENTRIES)
    .map((w) => `- ${w.h} (${w.i || "no IPA"}) = ${w.e || "(no meaning)"}`)
    .join("\n");

  return [
    {
      role: "system",
      content:
        "You are a helpful translator for a Hungarian vocabulary app. Translate the user's text into natural, conversational language. Use the provided wordlist as a reference for meanings and spelling, but you may produce natural sentences that include words not in the list. Provide a brief, helpful explanation of the translation when useful. Keep responses concise.",
    },
    {
      role: "user",
      content: `Translate the following ${sourceLang} text into ${targetLang}.

Input: """${text}"""

Relevant wordlist entries (for reference):
${dictText || "(none found)"}

Return ONLY a JSON object with two fields: "translation" (the translated text) and "explanation" (a short, helpful note about the translation or word choices). Do not include markdown or any other text.`,
    },
  ];
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { text, direction, dictionary } = req.body || {};

  if (!text || typeof text !== "string") {
    return res.status(400).json({ error: "Missing text" });
  }
  if (text.length > MAX_INPUT_LENGTH) {
    return res.status(400).json({ error: "Input too long" });
  }
  if (!["auto", "en2hu", "hu2en", "vi2hu"].includes(direction)) {
    return res.status(400).json({ error: "Invalid direction" });
  }

  const apiKey = process.env.OPENAI_API_KEY;
  const baseUrl = process.env.OPENAI_BASE_URL || "https://api.openai.com";
  const model = process.env.OPENAI_MODEL || "gpt-3.5-turbo";

  if (!apiKey) {
    return res.status(500).json({ error: "Translation API not configured" });
  }

  try {
    const messages = buildPrompt(text, direction, dictionary || []);

    const response = await fetch(`${baseUrl}/v1/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages,
        temperature: 0.5,
        max_tokens: 512,
      }),
    });

    if (!response.ok) {
      const err = await response.text();
      throw new Error(`API error: ${response.status} ${err}`);
    }

    const data = await response.json();
    const content = data.choices?.[0]?.message?.content?.trim() || "";

    let parsed;
    try {
      // Remove possible markdown fences
      const clean = content.replace(/^```json\s*/i, "").replace(/\s*```$/, "");
      parsed = JSON.parse(clean);
    } catch (e) {
      // Fallback: treat the whole response as the translation
      parsed = { translation: content, explanation: "" };
    }

    return res.status(200).json({
      translation: parsed.translation || content,
      explanation: parsed.explanation || "",
      sourceLanguage: detectLanguage(text),
    });
  } catch (err) {
    console.error("[translate]", err);
    return res.status(500).json({ error: err.message || "Translation failed" });
  }
}
