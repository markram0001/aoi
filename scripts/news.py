import pandas as pd
import requests
import re
import os
from datetime import date
from io import StringIO

# -----------------------------
# CONFIG
# -----------------------------

KEYWORD_PATTERNS = [
    r"\bai\b",
    r"\bartificial intelligence\b",
    r"\bagi\b",
    r"\bgenai\b",
    r"\bgenerative ai\b",

    r"\bopenai\b",
    r"\banthropic\b",
    r"\bdeepmind\b",
    r"\bgoogle deepmind\b",
    r"\bmicrosoft\b",
    r"\bmeta\b",
    r"\bnvidia\b",
    r"\bxai\b",

    r"\bchatgpt\b",
    r"\bgpt[- ]?\d+\b",
    r"\bgpt\b",
    r"\bclaude\b",
    r"\bgemini\b",
    r"\bgemma\b",
    r"\bllama\b",
    r"\bqwen\b",
    r"\bdeepseek\b",

    r"\bai model\b",
    r"\blarge language model\b",
    r"\bllm\b"
]

HEADERS = {"User-Agent": "ai-panic-index/0.1"}

# -----------------------------
# Helper
# -----------------------------

def title_matches(title):
    t = title.lower()
    return any(re.search(p, t) for p in KEYWORD_PATTERNS)

# -----------------------------
# Load latest GDELT GKG file
# -----------------------------

gdelt_url = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"

resp = requests.get(gdelt_url, headers=HEADERS)
resp.raise_for_status()

# ✅ CHANGED: use the FULL URL provided by lastupdate.txt
gkg_url = resp.text.strip().split("\n")[0].split(" ")[2]

csv_resp = requests.get(gkg_url, headers=HEADERS)
csv_resp.raise_for_status()

df = pd.read_csv(
    StringIO(csv_resp.text),
    sep="\t",
    header=None,
    low_memory=False
)

# Column 28 = best available headline proxy
titles = df[28].dropna().astype(str)

# -----------------------------
# Compute metrics
# -----------------------------

total_headlines = len(titles)

ai_headlines = [
    t for t in titles
    if title_matches(t)
]

ai_count = len(ai_headlines)
ai_share_pct = (ai_count / total_headlines) * 100 if total_headlines > 0 else 0

# -----------------------------
# Save summary CSV
# -----------------------------

summary_path = "data/news_ai_headline_summary.csv"

summary_row = pd.DataFrame([{
    "date": date.today().isoformat(),
    "total_headlines": total_headlines,
    "ai_headlines": ai_count,
    "ai_share_pct": ai_share_pct
}])

if os.path.exists(summary_path):
    df_summary = pd.read_csv(summary_path)
    df_summary = pd.concat([df_summary, summary_row], ignore_index=True)
else:
    df_summary = summary_row

df_summary.to_csv(summary_path, index=False)
