import json
import pandas as pd
import os

# -----------------------------
# Load reddit.json
# -----------------------------
with open("data/reddit.json", "r", encoding="utf-8") as f:
    dat = json.load(f)

date_str = dat["date"]
r = dat["reddit"]

# -----------------------------
# Extract scalars
# -----------------------------
total_points = r["total_points_top100"]
ai_points = r["ai_points_top100"]

# -----------------------------
# Extract vectors
# -----------------------------
all_scores_top100 = r["all_scores_top100"]
ai_scores_all = r["ai_scores_all"]

# -----------------------------
# Helper: append scalar as rows
# -----------------------------
def update_scalar_csv(path, date, value):
    row = pd.DataFrame([{
        "date": date,
        "value": value
    }])

    if os.path.exists(path):
        df = pd.read_csv(path)
        df = pd.concat([df, row]).drop_duplicates(
            subset=["date"],
            keep="last"
        )
    else:
        df = row

    df.to_csv(path, index=False)

# -----------------------------
# Helper: append vector as column
# -----------------------------
def update_vector_csv(path, date, values):
    series = pd.Series(values)

    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame()

    df[date] = series
    df.to_csv(path, index=False)

# -----------------------------
# Write scalar CSVs
# -----------------------------
update_scalar_csv(
    "data/total_points_top100.csv",
    date_str,
    total_points
)

update_scalar_csv(
    "data/ai_points_top100.csv",
    date_str,
    ai_points
)

# -----------------------------
# Write vector CSVs
# -----------------------------
update_vector_csv(
    "data/all_scores_top100.csv",
    date_str,
    all_scores_top100
)

update_vector_csv(
    "data/ai_scores_all.csv",
    date_str,
    ai_scores_all
)

print("✅ CSV extraction complete")
