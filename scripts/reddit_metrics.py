import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# -----------------------------
# Load today's JSON
# -----------------------------
with open("data/reddit.json", "r", encoding="utf-8") as f:
    dat = json.load(f)

r = dat["reddit"]

# Extract date (unchanged for plotting)
the_date = pd.to_datetime(dat["date"]).date()
date_col = dat["date"]  # STRING for CSV column header

# -----------------------------
# Compute metrics
# -----------------------------
total_points = r["total_points_top100"]
ai_points = r["ai_points_top100"]

X1 = ai_points / total_points
X2 = r["ai_count_top100"]

# Score distributions (vectors)
dist_overall = r["all_scores_top100"]
dist_ai = r["ai_scores_all"]

# -----------------------------
# NEW: write vectors as column-based CSVs
# -----------------------------

# ---- total_points.csv (Top 100 overall scores) ----
total_path = "data/total_points.csv"
try:
    total_df = pd.read_csv(total_path)
except FileNotFoundError:
    total_df = pd.DataFrame()

total_df[date_col] = pd.Series(dist_overall)
total_df.to_csv(total_path, index=False)

# ---- ai_points.csv (AI scores) ----
ai_path = "data/ai_points.csv"
try:
    ai_df = pd.read_csv(ai_path)
except FileNotFoundError:
    ai_df = pd.DataFrame()

ai_df[date_col] = pd.Series(dist_ai)
ai_df.to_csv(ai_path, index=False)

# -----------------------------
# Update daily.csv (unchanged)
# -----------------------------
today_row = pd.DataFrame([{
    "date": the_date,
    "X1": X1,
    "X2": X2
}])

csv_path = "data/daily.csv"

if os.path.exists(csv_path):
    daily = pd.read_csv(csv_path, parse_dates=["date"])
    daily = pd.concat([daily, today_row]).drop_duplicates()
else:
    daily = today_row

daily.to_csv(csv_path, index=False)

# -----------------------------
# Save plots into data/
# -----------------------------
sns.set_theme(style="whitegrid")

# Density plot
df_density = pd.DataFrame({
    "score": dist_overall + dist_ai,
    "group": (["Overall Top 100"] * len(dist_overall)) +
             (["AI All"] * len(dist_ai))
})

plt.figure(figsize=(8, 5))
sns.kdeplot(data=df_density, x="score", hue="group", fill=True, alpha=0.4)
plt.title("Density of Upvotes")
plt.xlabel("Score (Upvotes)")
plt.ylabel("Density")
plt.tight_layout()
plt.savefig("data/density_plot.png", dpi=300)
plt.close()

# X1 time series
plt.figure(figsize=(8, 5))
plt.plot(daily["date"], daily["X1"], marker="o", color="steelblue")
plt.title("Daily X1 (AI Upvote Share)")
plt.xlabel("Date")
plt.ylabel("X1")
plt.tight_layout()
plt.savefig("data/X1_timeseries.png", dpi=300)
plt.close()

# X2 time series
plt.figure(figsize=(8, 5))
plt.plot(daily["date"], daily["X2"], marker="o", color="darkred")
plt.title("Daily X2 (AI Hits in Top 100)")
plt.xlabel("Date")
plt.ylabel("X2")
plt.tight_layout()
plt.savefig("data/X2_timeseries.png", dpi=300)
plt.close()
