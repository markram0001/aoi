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
# (UNCHANGED)
# -----------------------------
total_points = r["total_points_top100"]
ai_points = r["ai_points_top100"]

# ✅ NEW: extract AI count in Top 100
ai_count_top100 = r["ai_count_top100"]

all_scores_top100 = r["all_scores_top100"]
ai_scores_all = r["ai_scores_all"]

# -----------------------------
# Append scalar datasets (row-wise, no dedup)
# -----------------------------
def append_scalar_dataset(path, date, value):
    new_row = pd.DataFrame([{
        "date": date,
        "value": value
    }])

    if os.path.exists(path):
        df = pd.read_csv(path)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row

    df.to_csv(path, index=False)

# -----------------------------
# Append vector datasets (column-wise)
# -----------------------------
def append_vector_dataset(path, date, values):
    series = pd.Series(values)

    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame()

    df.insert(len(df.columns), date, series)  # keeps duplicate columns
    df.to_csv(path, index=False)

# -----------------------------
# Apply updates
# -----------------------------

# Scalars
append_scalar_dataset(
    "data/total_points_top100.csv",
    date_str,
    total_points
)

append_scalar_dataset(
    "data/ai_points_top100.csv",
    date_str,
    ai_points
)

# ✅ NEW: AI count in Top 100
append_scalar_dataset(
    "data/ai_count_top100.csv",
    date_str,
    ai_count_top100
)

# Vectors
append_vector_dataset(
    "data/all_scores_top100.csv",
    date_str,
    all_scores_top100
)

append_vector_dataset(
    "data/ai_scores_all.csv",
    date_str,
    ai_scores_all
)

print("✅ Datasets appended (duplicates allowed)")
