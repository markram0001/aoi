import requests
import json
import re
from datetime import date

# ---------------------------------------
# CONFIG
# ---------------------------------------

KEYWORD_PATTERNS = [
    r"\bai\b",
    r"\bartificial intelligence\b",
    r"\bagi\b",
    r"\bgenai\b",
    r"\bgenerative ai\b",

    # Labs
    r"\bopenai\b",
    r"\banthropic\b",
    r"\bdeepmind\b",
    r"\bgoogle deepmind\b",
    r"\bmicrosoft\b",
    r"\bmeta\b",
    r"\bnvidia\b",
    r"\bxai\b",

    # Models
    r"\bchatgpt\b",
    r"\bgpt[- ]?\d+\b",
    r"\bgpt\b",
    r"\bclaude\b",
    r"\bsonnet\b",
    r"\bhaiku\b",
    r"\bopus\b",
    r"\bgemini\b",
    r"\bgemini \d+\b",
    r"\bgemma\b",
    r"\bllama\b",
    r"\bllama \d+\b",
    r"\bllama\d+\b",
    r"\bqwen\b",
    r"\bqwen\d+\b",
    r"\bdeepseek\b",
    r"\bdeepseek[- ]?v?\d*\b",

    # Ecosystem terms
    r"\bai model\b",
    r"\blarge language model\b",
    r"\bllm\b"
]

HEADERS = {"User-Agent": "ai-panic-index/0.1"}


# ---------------------------------------
# HELPERS
# ---------------------------------------

def extract_search_terms():
    terms = []
    for p in KEYWORD_PATTERNS:
        # Remove regex anchors and special characters
        term = re.sub(r"\\b", "", p)          # remove \b
        term = re.sub(r"\\d\+", "", term)     # remove \d+
        term = re.sub(r"[-?^$*+]", " ", term) # remove regex operators
        term = term.strip()
        if term:
            terms.append(term)
    return terms


def fetch_json(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def title_matches(title):
    t = title.lower()
    return any(re.search(pattern, t) for pattern in KEYWORD_PATTERNS)


# ---------------------------------------
# 1 & 2: TOP 100 POSTS
# ---------------------------------------

def analyze_top100():
    url = "https://www.reddit.com/r/all/top.json?limit=100&t=day"
    data = fetch_json(url)
    posts = data["data"]["children"]

    total_points_top100 = 0
    ai_points_top100 = 0
    ai_count_top100 = 0

    ai_posts_top100 = []
    all_top100_posts = []   # NEW: store all posts

    for p in posts:
        score = p["data"]["score"]
        title = p["data"]["title"]

        total_points_top100 += score

        # Store all posts
        all_top100_posts.append({
            "title": title,
            "score": score
        })

        # AI matching
        if title_matches(title):
            ai_points_top100 += score
            ai_count_top100 += 1
            ai_posts_top100.append({
                "title": title,
                "score": score
            })

    # Sort both lists by score descending
    all_top100_posts.sort(key=lambda x: x["score"], reverse=True)
    ai_posts_top100.sort(key=lambda x: x["score"], reverse=True)

    # Score vectors
    ai_scores_top100 = [p["score"] for p in ai_posts_top100]
    all_scores_top100 = [p["score"] for p in all_top100_posts]

    return (
        total_points_top100,
        ai_points_top100,
        ai_count_top100,
        ai_posts_top100,
        ai_scores_top100,
        all_top100_posts,
        all_scores_top100
    )


# ---------------------------------------
# 3: ALL AI POSTS (first 100 search results)
# ---------------------------------------

def analyze_all_ai_posts():
    query = "+".join(["ai", "artificial intelligence", "agi", "openai", "chatgpt"])
    url = f"https://www.reddit.com/search.json?q={query}&limit=100&sort=top&t=week"
    data = fetch_json(url)
    posts = data["data"]["children"]

    ai_points_all = 0
    ai_count_all = 0
    ai_posts_all = []

    for p in posts:
        score = p["data"]["score"]
        title = p["data"]["title"]

        if title_matches(title):
            ai_points_all += score
            ai_count_all += 1
            ai_posts_all.append({
                "title": title,
                "score": score
            })

    # Sort by score descending
    ai_posts_all.sort(key=lambda x: x["score"], reverse=True)

    # Score vector
    ai_scores_all = [p["score"] for p in ai_posts_all]

    return ai_points_all, ai_count_all, ai_posts_all, ai_scores_all


# ---------------------------------------
# MAIN
# ---------------------------------------

def main():
    (
        total_points_top100,
        ai_points_top100,
        ai_count_top100,
        ai_posts_top100,
        ai_scores_top100,
        all_top100_posts,
        all_scores_top100
    ) = analyze_top100()

    (
        ai_points_all,
        ai_count_all,
        ai_posts_all,
        ai_scores_all
    ) = analyze_all_ai_posts()

    out = {
        "date": str(date.today()),
        "reddit": {
            "total_points_top100": total_points_top100,
            "ai_points_top100": ai_points_top100,
            "ai_count_top100": ai_count_top100,
            "ai_posts_top100": ai_posts_top100,
            "ai_scores_top100": ai_scores_top100,

            # NEW: full sorted top 100
            "all_top100_posts": all_top100_posts,
            "all_scores_top100": all_scores_top100,

            "ai_points_all": ai_points_all,
            "ai_count_all": ai_count_all,
            "ai_posts_all": ai_posts_all,
            "ai_scores_all": ai_scores_all
        }
    }

    with open("data/reddit.json", "w") as f:
        json.dump(out, f, indent=2)

    print("Wrote data/reddit.json")


if __name__ == "__main__":
    main()
