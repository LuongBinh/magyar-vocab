import { useEffect, useState } from "react";
import Head from "next/head";
import { wordDatabase } from "@/lib/words";
import Translator from "@/components/Translator";

export default function Home() {
  const [activeTab, setActiveTab] = useState("all");

  useEffect(() => {
    if (typeof window === "undefined") return;

    const ALLOWED_KEYS = new Set(["huTheme"]);

    function cleanupOldSessions() {
      const toRemove = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && !ALLOWED_KEYS.has(key)) toRemove.push(key);
      }
      toRemove.forEach((k) => localStorage.removeItem(k));
      if (toRemove.length) console.log(`[cleanup] Removed ${toRemove.length} stale localStorage key(s):`, toRemove);
    }

    const state = {
      currentView: "cards",
      currentTab: "all",
      searchQuery: "",
      selectedLetter: null,
      selectedDifficulty: null,
      theme: localStorage.getItem("huTheme") || "light",
    };

    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

    function getDifficulty(w) {
      if (w.e && w.e !== "(Hungarian word)") {
        return w.e.includes(";") ? "medium" : "easy";
      }
      return "hard";
    }

    function getFilteredWords() {
      let words = wordDatabase;

      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase();
        words = words.filter(
          (w) =>
            w.h.toLowerCase().includes(q) ||
            (w.e && w.e.toLowerCase().includes(q)) ||
            (w.i && w.i.toLowerCase().includes(q))
        );
      }
      if (state.selectedLetter) {
        words = words.filter((w) => {
          const first =
            w.h.normalize("NFD").replace(/[\u0300-\u036f]/g, "")[0] || w.h[0];
          return first.toUpperCase() === state.selectedLetter;
        });
      }
      if (state.selectedDifficulty) {
        words = words.filter((w) => getDifficulty(w) === state.selectedDifficulty);
      }
      return words;
    }

    function render() {
      const words = getFilteredWords();

      const countEl = document.getElementById("resultCount");
      if (countEl) countEl.innerHTML = `Showing <strong>${words.length}</strong> words`;

      if (state.currentView === "cards") renderCards(words);
      else renderList(words);
    }

    function renderCards(words) {
      const grid = document.getElementById("wordGrid");
      if (!grid) return;
      if (!words.length) {
        grid.innerHTML = emptyHTML();
        return;
      }
      grid.innerHTML = words
        .map((w) => {
          const diff = getDifficulty(w);
          const hasMeaning = w.e && w.e !== "(Hungarian word)";
          const ipa = w.i || "";
          return `
            <div class="word-card" data-word="${w.h}">
              <div class="word-header">
                <span class="word">${w.h}</span>
              </div>
              ${ipa ? `<div class="ipa">${ipa}</div>` : ""}
              <div class="meaning ${hasMeaning ? "" : "no-meaning"}">${hasMeaning ? w.e : "—"}</div>
              ${w.m ? `<div class="mnemonic"><span class="mnemonic-label">Mnemonic</span>${w.m}</div>` : ""}
              <div class="card-footer">
                <span class="difficulty-badge ${diff}">${diff === "easy" ? "Common" : diff === "medium" ? "Medium" : "Rare"}</span>
              </div>
            </div>`;
        })
        .join("");
    }

    function renderList(words) {
      const list = document.getElementById("listView");
      if (!list) return;
      if (!words.length) {
        list.innerHTML = emptyHTML();
        return;
      }
      list.innerHTML = words
        .map((w) => {
          const hasMeaning = w.e && w.e !== "(Hungarian word)";
          const ipa = w.i || "";
          return `
            <div class="list-item">
              <span class="word">${w.h}</span>
              ${ipa ? `<span class="ipa">${ipa}</span>` : ""}
              <span class="meaning ${hasMeaning ? "" : "no-meaning"}">${hasMeaning ? w.e : "—"}</span>
            </div>`;
        })
        .join("");
    }

    function emptyHTML(msg = "No words match your filters") {
      return `<div class="empty-state"><div class="icon">🔍</div><h3>${msg}</h3><p>Try adjusting your search or filters</p></div>`;
    }

    function onSearch(e) {
      state.searchQuery = e.target.value;
      const clearBtn = document.getElementById("searchClear");
      if (clearBtn) clearBtn.style.display = state.searchQuery ? "block" : "none";
      render();
    }

    function onClearSearch() {
      state.searchQuery = "";
      const input = document.getElementById("searchInput");
      const clearBtn = document.getElementById("searchClear");
      if (input) input.value = "";
      if (clearBtn) clearBtn.style.display = "none";
      render();
    }

    function onLetterClick(letter) {
      if (letter === "") {
        state.selectedLetter = state.selectedLetter !== null ? null : "";
      } else {
        state.selectedLetter = state.selectedLetter === letter ? null : letter;
      }
      $$("#alphaIndex .alpha-btn").forEach((b) => {
        const isActive = state.selectedLetter === null
          ? b.dataset.letter === ""
          : b.dataset.letter === state.selectedLetter;
        b.classList.toggle("active", isActive);
      });
      $$("#alphaFloatInner .alpha-float-btn").forEach((b) => {
        const isActive = state.selectedLetter === null
          ? b.dataset.letter === ""
          : b.dataset.letter === state.selectedLetter;
        b.classList.toggle("active", isActive);
      });
      render();
    }

    function onDifficultyClick(diff) {
      state.selectedDifficulty = state.selectedDifficulty === diff ? null : diff;
      $$(".diff-btn").forEach((b) =>
        b.classList.toggle("active", b.dataset.diff === (state.selectedDifficulty || ""))
      );
      render();
    }

    function onTabClick(tab) {
      state.currentTab = tab;
      $$(".tab-btn").forEach((b) => b.classList.toggle("active", b.dataset.tab === tab));
      render();
      setActiveTab(tab);
    }

    function onViewClick(view) {
      state.currentView = view;
      $$(".view-btn").forEach((b) => b.classList.toggle("active", b.dataset.view === view));
      const grid = document.getElementById("wordGrid");
      const list = document.getElementById("listView");
      if (grid) grid.style.display = view === "cards" ? "" : "none";
      if (list) list.style.display = view === "list" ? "" : "none";
      render();
    }

    function onThemeToggle() {
      state.theme = state.theme === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", state.theme);
      localStorage.setItem("huTheme", state.theme);
      const toggleBtn = document.getElementById("themeToggle");
      if (toggleBtn) toggleBtn.textContent = state.theme === "light" ? "🌙" : "☀️";
    }

    function init() {
      cleanupOldSessions();

      document.documentElement.setAttribute("data-theme", state.theme);
      const toggleBtn = document.getElementById("themeToggle");
      if (toggleBtn) toggleBtn.textContent = state.theme === "light" ? "🌙" : "☀️";

      const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
      const counts = {};
      wordDatabase.forEach((w) => {
        const c = (
          w.h.normalize("NFD").replace(/[\u0300-\u036f]/g, "")[0] || w.h[0]
        ).toUpperCase();
        counts[c] = (counts[c] || 0) + 1;
      });
      let alphaHTML = `<button class="alpha-btn active" data-letter="">All <span class="count">(${wordDatabase.length})</span></button>`;
      letters.forEach((l) => {
        const c = counts[l] || 0;
        if (c > 0) {
          alphaHTML += `<button class="alpha-btn" data-letter="${l}">${l} <span class="count">(${c})</span></button>`;
        }
      });
      const alphaIndex = document.getElementById("alphaIndex");
      if (alphaIndex) alphaIndex.innerHTML = alphaHTML;

      let floatHTML = `<button class="alpha-float-btn active" data-letter="">All</button>`;
      letters.forEach((l) => {
        const c = counts[l] || 0;
        if (c > 0) {
          floatHTML += `<button class="alpha-float-btn" data-letter="${l}">${l}</button>`;
        }
      });
      const alphaFloatInner = document.getElementById("alphaFloatInner");
      if (alphaFloatInner) alphaFloatInner.innerHTML = floatHTML;

      const easy = wordDatabase.filter((w) => getDifficulty(w) === "easy").length;
      const medium = wordDatabase.filter((w) => getDifficulty(w) === "medium").length;
      const hard = wordDatabase.filter((w) => getDifficulty(w) === "hard").length;
      const diffAll = document.getElementById("diffAllCount");
      const easyCount = document.getElementById("easyCount");
      const mediumCount = document.getElementById("mediumCount");
      const hardCount = document.getElementById("hardCount");
      if (diffAll) diffAll.textContent = wordDatabase.length;
      if (easyCount) easyCount.textContent = easy;
      if (mediumCount) mediumCount.textContent = medium;
      if (hardCount) hardCount.textContent = hard;

      const grid = document.getElementById("wordGrid");
      const list = document.getElementById("listView");
      if (grid) grid.style.display = "";
      if (list) list.style.display = "none";

      const searchInput = document.getElementById("searchInput");
      const searchClear = document.getElementById("searchClear");
      if (searchInput) searchInput.addEventListener("input", onSearch);
      if (searchClear) searchClear.addEventListener("click", onClearSearch);

      if (alphaIndex) {
        alphaIndex.addEventListener("click", (e) => {
          const btn = e.target.closest(".alpha-btn");
          if (btn) onLetterClick(btn.dataset.letter);
        });
      }

      if (alphaFloatInner) {
        alphaFloatInner.addEventListener("click", (e) => {
          const btn = e.target.closest(".alpha-float-btn");
          if (btn) onLetterClick(btn.dataset.letter);
        });
      }

      const sidebarAlpha = document.getElementById("alphaIndex");
      const floatBar = document.getElementById("alphaFloat");
      if (sidebarAlpha && floatBar) {
        const observer = new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              floatBar.classList.toggle("visible", !entry.isIntersecting);
            });
          },
          { root: null, threshold: 0 }
        );
        observer.observe(sidebarAlpha);
      }

      const searchBar = document.querySelector(".search-bar");
      if (searchBar) {
        const toggleSearchFloat = () => {
          searchBar.classList.toggle("floating", window.scrollY > 120);
        };
        window.addEventListener("scroll", toggleSearchFloat, { passive: true });
        toggleSearchFloat();
      }

      const tabBar = document.getElementById("tabBar");
      if (tabBar) {
        const toggleTabBarFloat = () => {
          tabBar.classList.toggle("floating", window.scrollY > 120);
        };
        window.addEventListener("scroll", toggleTabBarFloat, { passive: true });
        toggleTabBarFloat();
      }

      $$(".diff-btn").forEach((btn) => {
        btn.addEventListener("click", () => onDifficultyClick(btn.dataset.diff));
      });

      $$(".tab-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
          const tab = btn.dataset.tab;
          if (tab === "translator") {
            setActiveTab("translator");
            $$(".tab-btn").forEach((b) => b.classList.toggle("active", b.dataset.tab === "translator"));
          } else {
            onTabClick(tab);
          }
        });
      });

      $$(".view-btn").forEach((btn) => {
        btn.addEventListener("click", () => onViewClick(btn.dataset.view));
      });

      if (toggleBtn) toggleBtn.addEventListener("click", onThemeToggle);

      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") onClearSearch();
      });

      render();
    }

    init();

  }, []);

  const handleTabClick = (tab) => {
    setActiveTab(tab);
    if (tab !== "translator") {
      document.querySelectorAll(".tab-btn").forEach((b) => {
        b.classList.toggle("active", b.dataset.tab === tab);
      });
      const event = new Event("click");
      const targetBtn = document.querySelector(`.tab-btn[data-tab="${tab}"]`);
      if (targetBtn) targetBtn.dispatchEvent(event);
    }
  };

  return (
    <>
      <Head>
        <title>Magyar Vocab — Hungarian Vocabulary with IPA, Meanings & Mnemonics</title>
        <meta name="description" content="Learn Hungarian vocabulary with IPA pronunciation, English meanings and memory aids. 4,550 words from everyday Hungarian." />
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+HK:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🇭🇺</text></svg>" />
      </Head>

      <header>
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">🇭🇺</span>
            <span className="logo-text">
              Magyar<span className="logo-accent">Vocab</span>
            </span>
          </div>
          <div className="header-controls">
            <span className="header-badge">4,550 words · IPA</span>
            <button className="theme-toggle" id="themeToggle" aria-label="Toggle theme">
              🌙
            </button>
          </div>
        </div>
      </header>

      <div className="main-container">
        <aside className="sidebar">
          <div className="sidebar-section">
            <div className="sidebar-title">Alphabet</div>
            <div className="alpha-index" id="alphaIndex"></div>
          </div>

          <div className="sidebar-section">
            <div className="sidebar-title">Difficulty</div>
            <div className="diff-filters">
              <button className="diff-btn active" data-diff="">
                <span className="diff-dot" style={{ background: "var(--text-light)" }}></span> All
                <span className="diff-count" id="diffAllCount">0</span>
              </button>
              <button className="diff-btn" data-diff="easy">
                <span className="diff-dot easy"></span> Common
                <span className="diff-count" id="easyCount">0</span>
              </button>
              <button className="diff-btn" data-diff="medium">
                <span className="diff-dot medium"></span> Medium
                <span className="diff-count" id="mediumCount">0</span>
              </button>
              <button className="diff-btn" data-diff="hard">
                <span className="diff-dot hard"></span> Rare
                <span className="diff-count" id="hardCount">0</span>
              </button>
            </div>
          </div>
        </aside>

        <main className="content-area">
          <div className="alpha-float" id="alphaFloat">
            <div className="alpha-float-inner" id="alphaFloatInner"></div>
          </div>

          <div className="tab-bar" id="tabBar">
            <button
              className={`tab-btn ${activeTab === "all" ? "active" : ""}`}
              data-tab="all"
              onClick={() => handleTabClick("all")}
            >
              All Words
            </button>
            <button
              className={`tab-btn ${activeTab === "translator" ? "active" : ""}`}
              data-tab="translator"
              onClick={() => handleTabClick("translator")}
            >
              Translator
            </button>
          </div>

          {activeTab !== "translator" && (
            <>
              <div className="search-bar">
                <svg className="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="8" />
                  <path d="m21 21-4.35-4.35" />
                </svg>
                <input type="text" id="searchInput" placeholder="Search Hungarian or English..." />
                <button className="clear-btn" id="searchClear" style={{ display: "none" }} aria-label="Clear search">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>

              <div className="stats-bar">
                <div className="count" id="resultCount">
                  Showing <strong>0</strong> words
                </div>
                <div className="view-toggles">
                  <button className="view-btn active" data-view="cards">
                    Cards
                  </button>
                  <button className="view-btn" data-view="list">
                    List
                  </button>
                </div>
              </div>

              <div className="tab-content">
                <div className="word-grid" id="wordGrid"></div>
                <div className="list-view" id="listView" style={{ display: "none" }}></div>
              </div>
            </>
          )}

          {activeTab === "translator" && <Translator />}
        </main>
      </div>

      <div className="toast" id="toast"></div>
    </>
  );
}
