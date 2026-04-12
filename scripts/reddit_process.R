library(jsonlite)
library(dplyr)
library(ggplot2)
library(readr)

# Load today's JSON
dat <- fromJSON("data/reddit.json")
r <- dat$reddit

# Extract date from JSON
the_date <- as.Date(dat$date)

# Compute metrics
total_points <- r$total_points_top100
ai_points <- r$ai_points_top100
X1 <- ai_points / total_points

X2 <- r$ai_count_top100

# Score distributions
dist_overall <- r$all_scores_top100
dist_ai <- r$ai_scores_top100

# Create a data frame for today's metrics
today_row <- tibble(
  date = the_date,
  X1 = X1,
  X2 = X2
)

# If daily.csv exists, append; otherwise create it
if (file.exists("data/daily.csv")) {
  daily <- read_csv("data/daily.csv", show_col_types = FALSE)
  daily <- bind_rows(daily, today_row) %>% distinct()
} else {
  daily <- today_row
}

# Save updated CSV
write_csv(daily, "data/daily.csv")

# Density plot: overall vs AI
df_density <- bind_rows(
  tibble(score = dist_overall, group = "Overall Top 100"),
  tibble(score = dist_ai, group = "AI Top 100")
)

ggplot(df_density, aes(x = score, fill = group)) +
  geom_density(alpha = 0.4) +
  scale_x_continuous(labels = scales::comma) +
  labs(
    title = "Density of Upvotes",
    x = "Score (Upvotes)",
    y = "Density",
    fill = "Group"
  ) +
  theme_minimal()

ggplot(daily, aes(x = date, y = X1)) +
  geom_line(color = "steelblue", size = 1.2) +
  geom_point(color = "steelblue") +
  labs(
    title = "Daily X1 (AI Upvote Share)",
    x = "Date",
    y = "X1"
  ) +
  theme_minimal()

ggplot(daily, aes(x = date, y = X2)) +
  geom_line(color = "darkred", size = 1.2) +
  geom_point(color = "darkred") +
  labs(
    title = "Daily X2 (AI Hits in Top 100)",
    x = "Date",
    y = "X2"
  ) +
  theme_minimal()

