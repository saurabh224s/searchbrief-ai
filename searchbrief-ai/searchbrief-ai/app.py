"""
SearchBrief AI - SerpApi India Hackathon 2026
A web app that searches the web using SerpApi and summarizes results using Claude AI.
"""

import os
import json
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ─── API Keys from environment variables ───────────────────────────────────────
SERPAPI_KEY     = os.environ.get("SERPAPI_KEY", "")
ANTHROPIC_KEY   = os.environ.get("ANTHROPIC_API_KEY", "")

# ─── SerpApi search function ───────────────────────────────────────────────────
def search_web(query, num_results=10):
    """
    Searches Google via SerpApi and returns a list of result dicts.
    Each dict has: title, link, snippet
    """
    url = "https://serpapi.com/search"
    params = {
        "q":        query,
        "api_key":  SERPAPI_KEY,
        "engine":   "google",
        "num":      num_results,
        "hl":       "en",
        "gl":       "in",   # India locale
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("organic_results", []):
        results.append({
            "title":   item.get("title", ""),
            "link":    item.get("link", ""),
            "snippet": item.get("snippet", ""),
        })

    # Also grab "answer box" or "knowledge graph" if present
    extra = ""
    if "answer_box" in data:
        box = data["answer_box"]
        extra = box.get("answer") or box.get("snippet") or ""
    elif "knowledge_graph" in data:
        kg = data["knowledge_graph"]
        extra = kg.get("description", "")

    return results, extra


# ─── Claude AI summarize function ─────────────────────────────────────────────
def summarize_with_claude(query, results, extra_answer):
    """
    Sends search results to Claude claude-sonnet-4-6 and gets back a structured
    research brief as plain text / markdown.
    """
    # Build context from search results
    results_text = ""
    for i, r in enumerate(results, 1):
        results_text += f"\n[{i}] {r['title']}\n    URL: {r['link']}\n    {r['snippet']}\n"

    if extra_answer:
        results_text = f"FEATURED ANSWER:\n{extra_answer}\n\n" + results_text

    prompt = f"""You are an expert research analyst. A user searched for: "{query}"

Here are the top web search results:
{results_text}

Write a clear, structured research brief based ONLY on these results. Use this exact format:

## 🔍 Research Brief: {query}

### Key Takeaway
(1–2 sentence summary of the most important finding)

### What We Know
(3–5 bullet points of the most important facts from the search results)

### Key Sources
(List the top 3 most relevant sources with their titles and URLs)

### Quick Context
(2–3 sentences of background context that helps understand the topic)

### What to Explore Next
(2–3 suggested follow-up questions or angles to investigate)

Be concise, factual, and directly useful. Do not add disclaimers or padding."""

    headers = {
        "x-api-key":         ANTHROPIC_KEY,
        "anthropic-version": "2023-06-01",
        "content-type":      "application/json",
    }
    body = {
        "model":      "claude-sonnet-4-6",
        "max_tokens": 1000,
        "messages":   [{"role": "user", "content": prompt}],
    }

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["content"][0]["text"]


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    """Main search + summarize endpoint. Returns JSON."""
    data = request.get_json()
    query = (data.get("query") or "").strip()

    if not query:
        return jsonify({"error": "Please enter a search topic."}), 400

    if not SERPAPI_KEY:
        return jsonify({"error": "SERPAPI_KEY is not set. See setup instructions."}), 500

    if not ANTHROPIC_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY is not set. See setup instructions."}), 500

    try:
        # Step 1: Search the web
        results, extra = search_web(query)

        if not results:
            return jsonify({"error": "No search results found. Try a different query."}), 404

        # Step 2: Summarize with Claude
        brief = summarize_with_claude(query, results, extra)

        return jsonify({
            "brief":   brief,
            "sources": results[:5],   # send top 5 sources to frontend
            "query":   query,
        })

    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            return jsonify({"error": "Invalid API key. Check your SERPAPI_KEY or ANTHROPIC_API_KEY."}), 401
        return jsonify({"error": f"API error: {str(e)}"}), 500

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Please try again."}), 504

    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500


# ─── Health check endpoint ─────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({
        "status":        "ok",
        "serpapi_key":   "set" if SERPAPI_KEY   else "missing",
        "anthropic_key": "set" if ANTHROPIC_KEY else "missing",
    })


if __name__ == "__main__":
    # Check keys on startup
    if not SERPAPI_KEY:
        print("⚠️  WARNING: SERPAPI_KEY environment variable is not set.")
    if not ANTHROPIC_KEY:
        print("⚠️  WARNING: ANTHROPIC_API_KEY environment variable is not set.")
    print("🚀 SearchBrief AI running at http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
