/**
 * SearchBrief AI — Frontend Logic
 * Handles search submission, loading states, markdown rendering, and error display.
 */

// ── DOM references ────────────────────────────────────────────────────────────
const queryInput    = document.getElementById("queryInput");
const searchBtn     = document.getElementById("searchBtn");
const loadingState  = document.getElementById("loadingState");
const loadingMsg    = document.getElementById("loadingMsg");
const errorState    = document.getElementById("errorState");
const errorMsg      = document.getElementById("errorMsg");
const briefCard     = document.getElementById("briefCard");
const briefBody     = document.getElementById("briefBody");
const sourcesList   = document.getElementById("sourcesList");
const howSection    = document.getElementById("howSection");

// ── Enter key support ─────────────────────────────────────────────────────────
queryInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") runSearch();
});

// ── State management ──────────────────────────────────────────────────────────
function showLoading(message) {
  loadingMsg.textContent = message;
  loadingState.hidden = false;
  errorState.hidden   = true;
  briefCard.hidden    = true;
  howSection.hidden   = true;
  searchBtn.disabled  = true;
  searchBtn.querySelector(".btn-text").textContent = "Researching…";
}

function showError(message) {
  errorMsg.textContent  = message;
  errorState.hidden     = false;
  loadingState.hidden   = true;
  briefCard.hidden      = true;
  howSection.hidden     = false;
  searchBtn.disabled    = false;
  searchBtn.querySelector(".btn-text").textContent = "Research";
}

function showBrief(brief, sources, query) {
  // Render markdown-ish text to HTML
  briefBody.innerHTML = renderMarkdown(brief);

  // Render sources list
  sourcesList.innerHTML = "";
  sources.forEach((src, i) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span class="src-num">${i + 1}</span>
      <div class="src-info">
        <span class="src-title">${escapeHtml(src.title)}</span>
        <a class="src-link" href="${escapeHtml(src.link)}" target="_blank" rel="noopener">
          ${escapeHtml(src.link)}
        </a>
        ${src.snippet ? `<p class="src-snip">${escapeHtml(src.snippet)}</p>` : ""}
      </div>
    `;
    sourcesList.appendChild(li);
  });

  briefCard.hidden    = false;
  loadingState.hidden = true;
  errorState.hidden   = true;
  howSection.hidden   = true;

  searchBtn.disabled  = false;
  searchBtn.querySelector(".btn-text").textContent = "Research";

  // Scroll to brief
  briefCard.scrollIntoView({ behavior: "smooth", block: "start" });
}

function resetSearch() {
  briefCard.hidden    = true;
  errorState.hidden   = true;
  howSection.hidden   = false;
  queryInput.value    = "";
  queryInput.focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ── Main search function ──────────────────────────────────────────────────────
async function runSearch() {
  const query = queryInput.value.trim();

  if (!query) {
    queryInput.focus();
    queryInput.style.borderColor = "red";
    setTimeout(() => queryInput.style.borderColor = "", 1000);
    return;
  }

  showLoading("Searching the web via SerpApi…");

  // Brief loading message sequence
  const messages = [
    "Searching the web via SerpApi…",
    "Fetching top results…",
    "Asking Claude to write your brief…",
    "Almost ready…",
  ];
  let msgIndex = 0;
  const msgInterval = setInterval(() => {
    msgIndex = (msgIndex + 1) % messages.length;
    loadingMsg.textContent = messages[msgIndex];
  }, 1800);

  try {
    const response = await fetch("/search", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ query }),
    });

    const data = await response.json();
    clearInterval(msgInterval);

    if (!response.ok) {
      showError(data.error || "An unexpected error occurred. Please try again.");
      return;
    }

    showBrief(data.brief, data.sources, data.query);

  } catch (err) {
    clearInterval(msgInterval);
    showError("Could not connect to the server. Is the app running?");
    console.error(err);
  }
}

// ── Markdown renderer (minimal, covers Claude's output format) ────────────────
function renderMarkdown(text) {
  // Escape HTML first for safety
  let html = text
    // ## headings
    .replace(/^## (.+)$/gm, "<h2>$1</h2>")
    // ### headings
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    // **bold**
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    // *italic*
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    // - bullet list items
    .replace(/^\- (.+)$/gm, "<li>$1</li>")
    // Wrap consecutive <li> in <ul>
    .replace(/(<li>[\s\S]*?<\/li>)(?!\s*<li>)/g, (match) => `<ul>${match}</ul>`)
    // Blank lines → paragraph breaks
    .replace(/\n{2,}/g, "</p><p>")
    // Single newlines
    .replace(/\n/g, "<br />");

  // Wrap in paragraph if not already block element
  if (!html.startsWith("<h") && !html.startsWith("<ul") && !html.startsWith("<ol")) {
    html = `<p>${html}</p>`;
  }

  return html;
}

// ── HTML escape helper ────────────────────────────────────────────────────────
function escapeHtml(str) {
  const div = document.createElement("div");
  div.appendChild(document.createTextNode(String(str || "")));
  return div.innerHTML;
}
