# SearchBrief AI 🔍

**Research anything. Understand it instantly.**

SearchBrief AI fetches live Google search results via [SerpApi](https://serpapi.com) and uses [Anthropic's Claude](https://anthropic.com) to turn them into a clean, structured research brief — in seconds.

Built for the **SerpApi India Hackathon 2026**.

---

## What It Does

1. User types any topic into the search box
2. SerpApi fetches the top 10 live Google results
3. Claude AI reads those results and writes a structured brief containing:
   - Key takeaway
   - Important facts (bullet points)
   - Top sources with links
   - Background context
   - Suggested follow-up questions
4. The brief appears on the page instantly

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Python 3.11, Flask 3.0            |
| Search    | SerpApi — Google Search Engine    |
| AI        | Anthropic Claude (claude-sonnet-4-6) |
| Frontend  | HTML, CSS, Vanilla JavaScript     |

---

## Setup Instructions

### Step 1 — Install Python

Download Python 3.11 from [python.org/downloads](https://python.org/downloads).

During installation on Windows, **check the box "Add Python to PATH"**.

Verify it works by opening Command Prompt and typing:
```
python --version
```
You should see something like `Python 3.11.x`.

---

### Step 2 — Get Your API Keys

**SerpApi Key (free):**
1. Go to [serpapi.com](https://serpapi.com) and sign up for a free account
2. Log in → go to your Dashboard
3. Copy your **API Key** from the dashboard

**Anthropic API Key:**
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / Log in
3. Click **API Keys** → **Create Key**
4. Copy the key (you only see it once — save it in Notepad)

---

### Step 3 — Download and Set Up the Project

**Option A: Clone with Git**
```bash
git clone https://github.com/YOUR_USERNAME/searchbrief-ai.git
cd searchbrief-ai
```

**Option B: Download ZIP**
- Download the ZIP from GitHub → Extract it → Open the folder in Command Prompt

---

### Step 4 — Install Dependencies

In Command Prompt (inside the project folder):
```bash
pip install -r requirements.txt
```

---

### Step 5 — Set Your API Keys

**On Windows (Command Prompt):**
```cmd
set SERPAPI_KEY=your_serpapi_key_here
set ANTHROPIC_API_KEY=your_anthropic_key_here
```

**On Mac / Linux (Terminal):**
```bash
export SERPAPI_KEY=your_serpapi_key_here
export ANTHROPIC_API_KEY=your_anthropic_key_here
```

Replace `your_serpapi_key_here` and `your_anthropic_key_here` with your actual keys.

---

### Step 6 — Run the App

```bash
python app.py
```

You should see:
```
🚀 SearchBrief AI running at http://localhost:5000
```

---

### Step 7 — Open in Browser

Go to: **http://localhost:5000**

Type any topic and click **Research**. Your brief will appear in a few seconds.

---

## Project Structure

```
searchbrief-ai/
├── app.py              ← Flask backend (search + AI logic)
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
├── templates/
│   └── index.html      ← Main webpage
└── static/
    ├── style.css       ← Styling
    └── app.js          ← Frontend logic
```

---

## How SerpApi Is Used

The app calls SerpApi's **Google Search** endpoint (`/search?engine=google`) to retrieve real-time search results for any query the user enters. This is the core data source — without live search data, the AI has no current information to summarize.

API parameters used:
- `engine=google` — Google search
- `gl=in` — Results relevant to India
- `num=10` — Top 10 results
- `hl=en` — English language results

The app also uses `answer_box` and `knowledge_graph` fields from SerpApi responses when available, for richer summaries.

---

## Environment Variables

| Variable            | Description                          |
|---------------------|--------------------------------------|
| `SERPAPI_KEY`       | Your SerpApi API key (required)      |
| `ANTHROPIC_API_KEY` | Your Anthropic Claude key (required) |

---

## Troubleshooting

**"SERPAPI_KEY is not set" error:**
Run the `set` command again in the same Command Prompt window before running `python app.py`.

**"pip is not recognized":**
Python was not added to PATH. Reinstall Python and check "Add to PATH".

**Port already in use:**
Another app is using port 5000. Stop it, or change the port in `app.py`: `app.run(port=5001)`.

**No results returned:**
Check your SerpApi key is valid and you have remaining credits.

---

## License

MIT License — free to use, modify, and distribute.

---

*Built with SerpApi + Anthropic Claude · SerpApi India Hackathon 2026*
