import { useState, useMemo } from "react";
import { wordDatabase } from "@/lib/words";

const DIRECTIONS = {
  auto: { label: "Auto-detect", source: "auto", target: "Hungarian / English" },
  mixed2hu: { label: "English/Vietnamese → Hungarian", source: "mixed English/Vietnamese", target: "Hungarian" },
  hu2en: { label: "Hungarian → English", source: "Hungarian", target: "English" },
};

function findRelevantWords(input) {
  if (!input) return [];
  const lower = input.toLowerCase();
  const words = lower.split(/[^\p{L}\p{N}]+/u).filter(Boolean);
  const matched = new Set();

  for (const entry of wordDatabase) {
    const huForms = entry.h.toLowerCase().split(/[;\/,]/).map((s) => s.trim()).filter(Boolean);
    const enForms = entry.e
      ? entry.e.toLowerCase().split(/[;\/,]/).map((s) => s.trim()).filter(Boolean)
      : [];
    const allForms = [...huForms, ...enForms];
    if (allForms.some((form) => words.includes(form) || lower.includes(form))) {
      matched.add(entry);
    }
  }

  return [...matched].slice(0, 30);
}

export default function Translator() {
  const [input, setInput] = useState("");
  const [direction, setDirection] = useState("auto");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const relevantWords = useMemo(() => findRelevantWords(input), [input]);

  const handleTranslate = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: input.trim(),
          direction,
          dictionary: relevantWords.map((w) => ({ h: w.h, e: w.e, i: w.i })),
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Translation failed");
      }
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="translator">
      <div className="translator-card">
        <div className="translator-header">
          <label htmlFor="translator-direction">Direction</label>
          <select
            id="translator-direction"
            value={direction}
            onChange={(e) => setDirection(e.target.value)}
            className="translator-select"
          >
            {Object.entries(DIRECTIONS).map(([key, { label }]) => (
              <option key={key} value={key}>
                {label}
              </option>
            ))}
          </select>
        </div>

        <textarea
          className="translator-input"
          placeholder="Type English, Vietnamese, or mixed input..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          rows={4}
        />

        <button
          className="translator-btn"
          onClick={handleTranslate}
          disabled={loading || !input.trim()}
        >
          {loading ? "Translating..." : "Translate"}
        </button>

        {error && <div className="translator-error">{error}</div>}

        {result && (
          <div className="translator-result">
            <div className="translator-result-label">
              {DIRECTIONS[direction]?.target || "Translation"}
            </div>
            <div className="translator-result-text">{result.translation}</div>
            {result.explanation && (
              <div className="translator-explanation">{result.explanation}</div>
            )}
          </div>
        )}

        {relevantWords.length > 0 && (
          <div className="translator-dictionary">
            <div className="translator-dictionary-label">
              Wordlist references used ({relevantWords.length})
            </div>
            <div className="translator-dictionary-list">
              {relevantWords.map((w) => (
                <div key={w.h} className="translator-dictionary-item">
                  <span className="word">{w.h}</span>
                  <span className="ipa">{w.i}</span>
                  <span className="meaning">{w.e}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
