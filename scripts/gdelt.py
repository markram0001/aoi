import requests
import os
from datetime import date

# -----------------------------
# CONFIG
# -----------------------------

url = "https://api.gdeltproject.org/api/v2/doc/doc"

params = {
    "mode": "artlist",
    "maxrecords": 50,
    "sourcelang": "eng",
    "sort": "DateDesc",
    "format": "json"
}

today = date.today().isoformat()

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# -----------------------------
# Fetch data
# -----------------------------

res = requests.get(url, params=params)
res.raise_for_status()

if not res.text.strip():
    raise RuntimeError("GDELT returned empty response")

try:
    data = res.json()
except ValueError:
    raise RuntimeError(f"Non-JSON response from GDELT:\n{res.text[:500]}")

articles = data.get("articles", [])
total_hits = len(articles)

# -----------------------------
# Save summary CSV
# -----------------------------

summary_path = "data/gdelt_latest_summary.csv"
summary_row = f"{today},{total_hits}\n"

if not os.path.exists(summary_path):
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("date,total_articles\n")

with open(summary_path, "a", encoding="utf-8") as f:
    f.write(summary_row)

# -----------------------------
# Save detailed headlines
# -----------------------------

details_path = f"data/gdelt_latest_articles_{today}.txt"

with open(details_path, "w", encoding="utf-8") as f:
    f.write(f"Date: {today}\n")
    f.write(f"Number of articles: {total_hits}\n\n")

    for a in articles:
        f.write(f"{a.get('seendate')} - {a.get('title')}\n")
        f.write(f"{a.get('sourceCommonName')}\n")
        f.write(f"{a.get('url')}\n\n")
