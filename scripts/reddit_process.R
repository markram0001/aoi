library(jsonlite)

# Load your JSON file
dat <- fromJSON("data/reddit.json")

# Extract the reddit block
r <- dat$reddit

# -----------------------------
# X1: Proportion of AI upvotes
# -----------------------------

total_points <- r$total_points_top100
ai_points <- r$ai_points_top100

X1 <- ai_points / total_points

# -----------------------------
# X2: Number of AI hits in top 100
# -----------------------------

X2 <- r$ai_count_top100

# -----------------------------
# Score distributions
# -----------------------------

# Distribution of scores from top 100 overall
dist_overall <- r$all_scores_top100

# Distribution of scores from top 100 AI posts
dist_ai <- r$ai_scores_top100

# Print results
list(
  X1 = X1,
  X2 = X2,
  overall_distribution = dist_overall,
  ai_distribution = dist_ai
)
