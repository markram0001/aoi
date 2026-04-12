import requests
import json
from datetime import date

# ---------------------------------------
# CONFIG
# ---------------------------------------

KEYWORDS = [
    "ai", "artificial intelligence", "agi",
    "openai", "chatgpt"
]

HEADERS = {"User-Agent": "ai-panic-index/0.1"}


# ---------------------------------------
# HELPERS
# ---------------------------------------

def fetch_json(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def title_matches(title):
    t = title.lower()
    return any(k in t for k in KEYWORDS)


# ---------------------------------------
# 1 & 2: TOP 100 POSTS
# ---------------------------------------

def analyze_top100():
    url = "https://www.reddit.com/r/all/top.json?limit=100&t=day"
    data = fetch_json(url)
    posts = data["data"]["children"]

    total_points_top100 = 0
    ai_points_top100 = 0

    for p in posts:
        score = p["data"]["score"]
        title = p["data"]["title"]

        total_points_top100 += score

        if title_matches(title):
            ai_points_top100 += score

    return total_points_top100, ai_points_top100


# ---------------------------------------
# 3: ALL AI POSTS (first 100 search results)
# ---------------------------------------

def analyze_all_ai_posts():
    # Search for ANY of the keywords
    # Reddit search is OR-based by default
    query = "+".join(KEYWORDS)
    url = f"https://www.reddit.com/search.json?q={query}&limit=100"
    data = fetch_json(url)
    posts = data["data"]["children"]

    ai_points_all = 0

    for p in posts:
        ai_points_all += p["data"]["score"]

    return ai_points_all


# ---------------------------------------
# MAIN
# ---------------------------------------

def main():
    total_points_top100, ai_points_top100 = analyze_top100()
    ai_points_all = analyze_all_ai_posts()

    out = {
        "date": str(date.today()),
        "reddit": {
            "total_points_top100": total_points_top100,
            "ai_points_top100": ai_points_top100,
            "ai_points_all": ai_points_all
        }
    }

    with open("data/reddit.json", "w") as f:
        json.dump(out, f, indent=2)

    print("Wrote data/reddit.json")


if __name__ == "__main__":
    main()
