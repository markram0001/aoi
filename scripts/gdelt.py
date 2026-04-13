import requests
from datetime import date

url = "https://api.gdeltproject.org/api/v2/doc/doc"

params = {
    "mode": "artlist",
    "maxrecords": 50,
    "sourcelang": "eng",
    "sort": "DateDesc",
    "format": "json"
}

res = requests.get(url, params=params)
res.raise_for_status()

# Defensive handling: GDELT may return non-JSON or empty
if not res.text.strip():
    print("GDELT returned empty response")
    exit(0)

try:
    data = res.json()
except ValueError:
    print("Non-JSON response from GDELT:")
    print(res.text[:500])
    exit(0)

articles = data.get("articles", [])

print("Date:", date.today().isoformat())
print("Number of articles returned:", len(articles))
print()

for a in articles:
    print(a.get("seendate"), "-", a.get("title"))
    print(a.get("sourceCommonName"))
    print(a.get("url"))
    print()
