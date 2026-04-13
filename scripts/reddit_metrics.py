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
# Extract present-day variables
# (DO NOT CHANGE THESE)
# -----------------------------
total_points = r["total_points_top100"]
ai_points = r["ai_points_top100"]

all_scores_top100 = r["all_scores_top100"]
ai_scores_all = r["ai_scores_all"]

# -----------------------------
# Update scalar datasets (row-wise)
# -----------------------------
def update_scalar_dataset(path, date, value):
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=["date", "value"])

    new_row = pd.DataFrame([{
        "date": date,
        "value": value
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    df = df.drop_duplicates(subset=["date"], keep="last")

    df.to_csv(path, index=False)

# -----------------------------
# Update vector datasets (column-wise)
# -----------------------------
def update_vector_dataset(path, date, values):
    series = pd.Series(values)

    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame()

    df[date] = series
    df.to_csv(path, index=False)

# -----------------------------
# Apply updates
# -----------------------------

# Scalars
update_scalar_dataset(
    "data/total_points_top100.csv",
    date_str,
    total_points
)

update_scalar_dataset(
    "data/ai_points_top100.csv",
    date_str,
    ai_points
)

# Vectors
update_vector_dataset(
    "data/all_scores_top100.csv",
    date_str,
    all_scores_top100
)

update_vector_dataset(
    "data/ai_scores_all.csv",
    date_str,
    ai_scores_all
)

print("✅ All datasets updated successfully")
