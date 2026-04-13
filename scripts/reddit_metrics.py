import json
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
ai_count_top100 = r["ai_count_top100"]

all_scores_top100 = r["all_scores_top100"]
ai_scores_all = r["ai_scores_all"]

# ✅ NEW: compute AI share percentage
ai_share_pct = (ai_points / total_points) * 100

# -----------------------------
# Append scalar datasets (row-wise, no dedup)
# -----------------------------
def append_scalar_dataset(path, row_dict):
    new_row = pd.DataFrame([row_dict])

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
        df.insert(len(df.columns), date, series, allow_duplicates=True)
    else:
        df = pd.DataFrame({date: series})

    df.to_csv(path, index=False)

# -----------------------------
# Apply updates
# -----------------------------

# Scalars (unchanged structure)
append_scalar_dataset(
    "data/total_points_top100.csv",
    {"date": date_str, "value": total_points}
)

append_scalar_dataset(
    "data/ai_points_top100.csv",
    {"date": date_str, "value": ai_points}
)

# ✅ CHANGED: ai_count + ai_share_pct in same CSV
append_scalar_dataset(
    "data/ai_count_top100.csv",
    {
        "date": date_str,
        "ai_count_top100": ai_count_top100,
        "ai_share_pct": ai_share_pct
    }
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

sns.set_theme(style="whitegrid")

# existing variables already in memory:
# all_scores_top100
# ai_scores_all

all_vals = np.array(all_scores_top100)
ai_vals = np.array(ai_scores_all)

plt.figure(figsize=(8, 5))
sns.kdeplot(all_vals, label="Overall Top 100", linewidth=2, alpha=0.7)
sns.kdeplot(ai_vals, label="AI (All)", linewidth=2, linestyle="--", alpha=0.7)

plt.title("Density of Reddit Upvotes")
plt.xlabel("Score (Upvotes)")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.savefig("data/density_plot.png", dpi=300)
plt.close()

import pandas as pd
import matplotlib.pyplot as plt

# load CSV produced by earlier script
df = pd.read_csv("data/ai_count_top100.csv")

# remove duplicate dates (keep last)
df = df.drop_duplicates(subset=["date"], keep="last")
df["date"] = pd.to_datetime(df["date"])

# --- AI count time series ---
plt.figure(figsize=(8, 5))
plt.plot(df["date"], df["ai_count_top100"], marker="o", color="darkred")
plt.title("AI Posts in Reddit Top 100")
plt.xlabel("Date")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("data/X1_timeseries.png", dpi=300)
plt.close()

# --- AI share % time series ---
plt.figure(figsize=(8, 5))
plt.plot(df["date"], df["ai_share_pct"], marker="o", color="steelblue")
plt.title("AI Share of Top 100 Upvotes (%)")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.tight_layout()
plt.savefig("data/X2_timeseries.png", dpi=300)
plt.close()
