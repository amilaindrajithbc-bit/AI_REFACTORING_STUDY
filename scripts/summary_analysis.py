import os
import pandas as pd

# ======================================================
# Configuration
# ======================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

METRICS_FILE = os.path.join(BASE_DIR, "metrics", "summary_results.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)

# ======================================================
# Load Dataset
# ======================================================
try:
    df = pd.read_csv(METRICS_FILE)
except FileNotFoundError:
    print(f"Error: File not found:\n{METRICS_FILE}")
    exit()

print("=" * 70)
print("Summary Dataset")
print("=" * 70)
print(df)

# ======================================================
# AI Models Only
# ======================================================
ai_df = df[df["Model"] != "Original"].copy()

# Convert numeric columns
numeric_columns = ["LOC", "CC", "MI", "Rank"]

for column in numeric_columns:
    ai_df[column] = pd.to_numeric(ai_df[column], errors="coerce")

print("\n")
print("=" * 70)
print("Cleaned AI Dataset")
print("=" * 70)
print(ai_df)

# ======================================================
# Average Metrics
# ======================================================
average_metrics = (
    ai_df.groupby("Model")[["LOC", "CC", "MI"]]
    .mean()
    .round(2)
    .sort_index()
)

print("\n")
print("=" * 70)
print("Average Metrics")
print("=" * 70)
print(average_metrics)

average_metrics.to_csv(
    os.path.join(RESULTS_DIR, "average_metrics.csv")
)

# ======================================================
# Win Count
# ======================================================
all_models = sorted(ai_df["Model"].unique())

win_count = (
    ai_df[ai_df["Rank"] == 1]
    .groupby("Model")
    .size()
    .reindex(all_models, fill_value=0)
    .reset_index(name="Wins")
)

print("\n")
print("=" * 70)
print("Win Count")
print("=" * 70)
print(win_count)

win_count.to_csv(
    os.path.join(RESULTS_DIR, "win_count.csv"),
    index=False,
)

# ======================================================
# Overall Ranking
# ======================================================
ranking = (
    ai_df.groupby("Model")["Rank"]
    .mean()
    .round(2)
    .reset_index()
    .rename(columns={"Rank": "Average Rank"})
    .sort_values("Average Rank")
)

print("\n")
print("=" * 70)
print("Overall Ranking")
print("=" * 70)
print(ranking)

ranking.to_csv(
    os.path.join(RESULTS_DIR, "overall_ranking.csv"),
    index=False,
)

# ======================================================
# Statistical Summary
# ======================================================
statistics = (
    ai_df.groupby("Model")[["LOC", "CC", "MI"]]
    .agg(["mean", "std", "min", "max"])
    .round(2)
)

print("\n")
print("=" * 70)
print("Statistical Summary")
print("=" * 70)
print(statistics)

statistics.to_csv(
    os.path.join(RESULTS_DIR, "statistical_summary.csv")
)

# ======================================================
# Best Model Per Metric
# ======================================================
best_loc = average_metrics["LOC"].idxmin()
best_cc = average_metrics["CC"].idxmin()
best_mi = average_metrics["MI"].idxmax()

best_metrics = pd.DataFrame(
    {
        "Metric": ["Lowest LOC", "Lowest CC", "Highest MI"],
        "Best Model": [best_loc, best_cc, best_mi],
    }
)

print("\n")
print("=" * 70)
print("Best Performing Models")
print("=" * 70)
print(best_metrics)

best_metrics.to_csv(
    os.path.join(RESULTS_DIR, "best_models.csv"),
    index=False,
)

# ======================================================
# Completion
# ======================================================
print("\n" + "=" * 70)
print("Analysis completed successfully.")
print("=" * 70)
print(f"Input File : {METRICS_FILE}")
print(f"Output Folder : {RESULTS_DIR}")

print("\nGenerated Files:")
print("- average_metrics.csv")
print("- win_count.csv")
print("- overall_ranking.csv")
print("- statistical_summary.csv")
print("- best_models.csv")