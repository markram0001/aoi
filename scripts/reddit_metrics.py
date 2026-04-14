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


ai_share_pct = (ai_points / total_points) * 100
ai_share_pct_top = (sum(ai_scores_all) / total_points) * 100


# Compute number of AI posts whose scores are within Top 100 threshold
top100_cutoff = min(all_scores_top100)
ai_within_top100 = sum(score >= top100_cutoff for score in ai_scores_all)

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

append_scalar_dataset(
    "data/total_points_top100.csv",
    {"date": date_str, "value": total_points}
)

append_scalar_dataset(
    "data/ai_points_top100.csv",
    {"date": date_str, "value": ai_points}
)

# Save both original AI count AND "within Top 100 threshold" count
append_scalar_dataset(
    "data/ai_count_top100.csv",
    {
        "date": date_str,
        "ai_count_top100": ai_count_top100,
        "ai_within_top100": ai_within_top100,
        "ai_share_pct": ai_share_pct,
        "ai_share_pct_top": ai_share_pct_top
    }
)

# Vectors (unchanged)
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

# -----------------------------
# Density plot (UNCHANGED)
# -----------------------------
sns.set_theme(style="whitegrid")

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

# -----------------------------
# Time series plots
# -----------------------------
df = pd.read_csv("data/ai_count_top100.csv")
df = df.drop_duplicates(subset=["date"], keep="last")
df["date"] = pd.to_datetime(df["date"])

# X1_timeseries now has TWO lines
plt.figure(figsize=(8, 5))
plt.plot(df["date"], df["ai_count_top100"],
         marker="o", label="AI posts in Top 100", color="darkred")
plt.plot(df["date"], df["ai_within_top100"],
         marker="o", label="AI posts with Top-100-level upvotes", color="steelblue")

plt.title("AI Presence in Reddit Top 100")
plt.xlabel("Date")
plt.ylabel("Count")
plt.legend()
plt.tight_layout()
plt.savefig("data/X1_timeseries.png", dpi=300)
plt.close()

# X2 (updated with two lines)
plt.figure(figsize=(8, 5))

plt.plot(
    df["date"],
    df["ai_share_pct"],
    marker="o",
    color="purple",
    label="AI Share (Observed in Top 100)"
)

plt.plot(
    df["date"],
    df["ai_share_pct_top"],
    marker="o",
    linestyle="--",
    color="darkgreen",
    label="AI Share (Observed in Top AI Search)"
)

plt.title("AI Share of Top 100 Upvotes (%)")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.legend()
plt.tight_layout()
plt.savefig("data/X2_timeseries.png", dpi=300)
plt.close()
