// ============================================================
// 🇭🇺 MAGYAR VOCAB — Hungarian Vocabulary App
// ============================================================

const App = (() => {
  "use strict";

  // ---------- State ----------
  const ALLOWED_KEYS = new Set(["huBookmarks", "huTheme"]);

  function cleanupOldSessions() {
    const toRemove = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && !ALLOWED_KEYS.has(key)) toRemove.push(key);
    }
    toRemove.forEach(k => localStorage.removeItem(k));
    if (toRemove.length) console.log(`[cleanup] Removed ${toRemove.length} stale localStorage key(s):`, toRemove);
  }

  const state = {
    currentView: "cards",
    currentTab: "all",
    searchQuery: "",
    selectedLetter: null,
    selectedDifficulty: null,
    bookmarks: new Set(JSON.parse(localStorage.getItem("huBookmarks") || "[]")),
    theme: localStorage.getItem("huTheme") || "light"
  };

  // ---------- DOM Helpers ----------
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  // ---------- Filter & Search ----------
  function getFilteredWords() {
    let words = wordDatabase;

    if (state.currentTab === "bookmarks") {
      words = words.filter(w => state.bookmarks.has(w.h));
    }
    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      words = words.filter(w =>
        w.h.toLowerCase().includes(q) ||
        (w.e && w.e.toLowerCase().includes(q)) ||
        (w.i && w.i.toLowerCase().includes(q))
      );
    }
    if (state.selectedLetter) {
      words = words.filter(w => {
        const first = w.h.normalize("NFD").replace(/[\u0300-\u036f]/g, "")[0] || w.h[0];
        return first.toUpperCase() === state.selectedLetter;
      });
    }
    if (state.selectedDifficulty) {
      words = words.filter(w => getDifficulty(w) === state.selectedDifficulty);
    }
    return words;
  }

  // Assign difficulty based on whether meaning exists
  function getDifficulty(w) {
    if (w.e && w.e !== "(Hungarian word)") {
      return w.e.includes(";") ? "medium" : "easy";
    }
    return "hard";
  }

  // ---------- Render ----------
  function render() {
    const words = getFilteredWords();

    // Update result count
    const label = state.currentTab === "bookmarks" ? "bookmarked" : "words";
    document.getElementById("resultCount").innerHTML =
      `Showing <strong>${words.length}</strong> ${label}`;

    if (state.currentView === "cards") renderCards(words);
    else renderList(words);
  }

  function renderCards(words) {
    const grid = document.getElementById("wordGrid");
    if (!words.length) {
      grid.innerHTML = emptyHTML();
      return;
    }
    grid.innerHTML = words.map(w => {
      const diff = getDifficulty(w);
      const hasMeaning = w.e && w.e !== "(Hungarian word)";
      const bookmarked = state.bookmarks.has(w.h);
      const ipa = w.i || "";
      return `
        <div class="word-card" data-word="${w.h}">
          <div class="word-header">
            <span class="word">${w.h}</span>
            <button class="bookmark-btn ${bookmarked ? 'bookmarked' : ''}"
                    onclick="App.toggleBookmark('${w.h}')">
              ${bookmarked ? '★' : '☆'}
            </button>
          </div>
          ${ipa ? `<div class="ipa">${ipa}</div>` : ''}
          <div class="meaning ${hasMeaning ? '' : 'no-meaning'}">${hasMeaning ? w.e : '—'}</div>
          ${w.m ? `<div class="mnemonic"><span class="mnemonic-label">Mnemonic</span>${w.m}</div>` : ''}
          <div class="card-footer">
            <span class="difficulty-badge ${diff}">${diff === 'easy' ? 'Common' : diff === 'medium' ? 'Medium' : 'Rare'}</span>
          </div>
        </div>`;
    }).join("");
  }

  function renderList(words) {
    const list = document.getElementById("listView");
    if (!words.length) {
      list.innerHTML = emptyHTML();
      return;
    }
    list.innerHTML = words.map(w => {
      const hasMeaning = w.e && w.e !== "(Hungarian word)";
      const bookmarked = state.bookmarks.has(w.h);
      const ipa = w.i || "";
      return `
        <div class="list-item">
          <span class="word">${w.h}</span>
          ${ipa ? `<span class="ipa">${ipa}</span>` : ''}
          <span class="meaning ${hasMeaning ? '' : 'no-meaning'}">${hasMeaning ? w.e : '—'}</span>
          <button class="bookmark-btn ${bookmarked ? 'bookmarked' : ''}"
                  onclick="App.toggleBookmark('${w.h}')">
            ${bookmarked ? '★' : '☆'}
          </button>
        </div>`;
    }).join("");
  }

  function emptyHTML(msg = "No words match your filters") {
    return `<div class="empty-state"><div class="icon">🔍</div><h3>${msg}</h3><p>Try adjusting your search or filters</p></div>`;
  }

  // ---------- Event Handlers ----------
  function onSearch(e) {
    state.searchQuery = e.target.value;
    document.getElementById("searchClear").style.display = state.searchQuery ? "block" : "none";
    render();
  }

  function onClearSearch() {
    state.searchQuery = "";
    document.getElementById("searchInput").value = "";
    document.getElementById("searchClear").style.display = "none";
    render();
  }

  function onLetterClick(letter) {
    if (letter === "") {
      state.selectedLetter = state.selectedLetter !== null ? null : "";
    } else {
      state.selectedLetter = state.selectedLetter === letter ? null : letter;
    }
    $$("#alphaIndex .alpha-btn").forEach(b => {
      const isActive = state.selectedLetter === null
        ? b.dataset.letter === ""
        : b.dataset.letter === state.selectedLetter;
      b.classList.toggle("active", isActive);
    });
    $$("#alphaFloatInner .alpha-float-btn").forEach(b => {
      const isActive = state.selectedLetter === null
        ? b.dataset.letter === ""
        : b.dataset.letter === state.selectedLetter;
      b.classList.toggle("active", isActive);
    });
    render();
  }

  function onDifficultyClick(diff) {
    state.selectedDifficulty = state.selectedDifficulty === diff ? null : diff;
    $$(".diff-btn").forEach(b => b.classList.toggle("active", b.dataset.diff === (state.selectedDifficulty || "")));
    render();
  }

  function onTabClick(tab) {
    state.currentTab = tab;
    $$(".tab-btn").forEach(b => b.classList.toggle("active", b.dataset.tab === tab));
    render();
  }

  function onViewClick(view) {
    state.currentView = view;
    $$(".view-btn").forEach(b => b.classList.toggle("active", b.dataset.view === view));
    document.getElementById("wordGrid").style.display = view === "cards" ? "" : "none";
    document.getElementById("listView").style.display = view === "list" ? "" : "none";
    render();
  }

  function onThemeToggle() {
    state.theme = state.theme === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", state.theme);
    localStorage.setItem("huTheme", state.theme);
    document.getElementById("themeToggle").textContent = state.theme === "light" ? "🌙" : "☀️";
  }

  // ---------- Public API ----------
  function toggleBookmark(word) {
    if (state.bookmarks.has(word)) {
      state.bookmarks.delete(word);
    } else {
      state.bookmarks.add(word);
    }
    localStorage.setItem("huBookmarks", JSON.stringify([...state.bookmarks]));
    render();
  }

  // ---------- Init ----------
  function init() {
    // Remove any old/stale localStorage keys from previous app versions
    cleanupOldSessions();

    // Apply theme
    document.documentElement.setAttribute("data-theme", state.theme);
    document.getElementById("themeToggle").textContent = state.theme === "light" ? "🌙" : "☀️";

    // Build alphabet index
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
    const counts = {};
    wordDatabase.forEach(w => {
      const c = (w.h.normalize("NFD").replace(/[\u0300-\u036f]/g, "")[0] || w.h[0]).toUpperCase();
      counts[c] = (counts[c] || 0) + 1;
    });
    let alphaHTML = `<button class="alpha-btn active" data-letter="">All <span class="count">(${wordDatabase.length})</span></button>`;
    letters.forEach(l => {
      const c = counts[l] || 0;
      if (c > 0) {
        alphaHTML += `<button class="alpha-btn" data-letter="${l}">${l} <span class="count">(${c})</span></button>`;
      }
    });
    document.getElementById("alphaIndex").innerHTML = alphaHTML;

    // Build floating alphabet bar
    let floatHTML = `<button class="alpha-float-btn active" data-letter="">All</button>`;
    letters.forEach(l => {
      const c = counts[l] || 0;
      if (c > 0) {
        floatHTML += `<button class="alpha-float-btn" data-letter="${l}">${l}</button>`;
      }
    });
    document.getElementById("alphaFloatInner").innerHTML = floatHTML;

    // Difficulty counts
    const easy = wordDatabase.filter(w => getDifficulty(w) === "easy").length;
    const medium = wordDatabase.filter(w => getDifficulty(w) === "medium").length;
    const hard = wordDatabase.filter(w => getDifficulty(w) === "hard").length;
    document.getElementById("diffAllCount").textContent = wordDatabase.length;
    document.getElementById("easyCount").textContent = easy;
    document.getElementById("mediumCount").textContent = medium;
    document.getElementById("hardCount").textContent = hard;

    // Set initial view
    document.getElementById("wordGrid").style.display = "";
    document.getElementById("listView").style.display = "none";

    // Event listeners
    document.getElementById("searchInput").addEventListener("input", onSearch);
    document.getElementById("searchClear").addEventListener("click", onClearSearch);

    document.getElementById("alphaIndex").addEventListener("click", e => {
      const btn = e.target.closest(".alpha-btn");
      if (btn) onLetterClick(btn.dataset.letter);
    });

    document.getElementById("alphaFloatInner").addEventListener("click", e => {
      const btn = e.target.closest(".alpha-float-btn");
      if (btn) onLetterClick(btn.dataset.letter);
    });

    // Show floating alphabet when sidebar alphabet scrolls out of view
    const sidebarAlpha = document.getElementById("alphaIndex");
    const floatBar = document.getElementById("alphaFloat");
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        floatBar.classList.toggle("visible", !entry.isIntersecting);
      });
    }, { root: null, threshold: 0 });
    observer.observe(sidebarAlpha);

    // Float search bar on scroll
    const searchBar = document.querySelector(".search-bar");
    const toggleSearchFloat = () => {
      searchBar.classList.toggle("floating", window.scrollY > 120);
    };
    window.addEventListener("scroll", toggleSearchFloat, { passive: true });
    toggleSearchFloat();

    $$(".diff-btn").forEach(btn => {
      btn.addEventListener("click", () => onDifficultyClick(btn.dataset.diff));
    });

    $$(".tab-btn").forEach(btn => {
      btn.addEventListener("click", () => onTabClick(btn.dataset.tab));
    });

    $$(".view-btn").forEach(btn => {
      btn.addEventListener("click", () => onViewClick(btn.dataset.view));
    });

    document.getElementById("themeToggle").addEventListener("click", onThemeToggle);

    document.addEventListener("keydown", e => {
      if (e.key === "Escape") onClearSearch();
    });

    render();
  }

  return { init, toggleBookmark };
})();

document.addEventListener("DOMContentLoaded", () => App.init());
