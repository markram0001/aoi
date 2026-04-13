import requests
from datetime import date

# -----------------------------
# CONFIG
# -----------------------------

QUERY = (
    '(AI OR "artificial intelligence" OR AGI OR GenAI OR "generative AI" '
    'OR OpenAI OR Anthropic OR DeepMind OR Microsoft OR Meta OR Nvidia OR xAI '
    'OR ChatGPT OR GPT OR Claude OR Gemini OR Gemma OR LLaMA OR Qwen OR DeepSeek '
    'OR "AI model" OR "large language model" OR LLM)'
)

params = {
    "query": QUERY,
    "mode": "artlist",
    "maxrecords": 50,
    "sourcelang": "eng",
    "sort": "DateDesc",
    "format": "json"
}

url = "https://api.gdeltproject.org/api/v2/doc/doc"

res = requests.get(url, params=params)
res.raise_for_status()

data = res.json()

# -----------------------------
# In-memory extracted data
# -----------------------------

articles = data.get("articles", [])
total_hits = len(articles)

headlines = [
    {
        "date": a.get("seendate"),
        "title": a.get("title"),
        "source": a.get("sourceCommonName"),
        "url": a.get("url")
    }
    for a in articles
]

# -----------------------------
# ✅ NEW: PRINT OUTPUT
# -----------------------------

print("Date:", date.today().isoformat())
print("Total AI-related news articles:", total_hits)
print()

for h in headlines:
    print(h["date"], "-", h["title"])
    print(h["source"])
    print(h["url"])
    print()
