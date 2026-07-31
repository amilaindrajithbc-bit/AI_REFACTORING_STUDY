"""
generate_graphs.py

Generate publication-quality figures for the
AI Refactoring Trustworthiness Study.

Author: Amila Piyasiri
Project:
Evaluating the Trustworthiness of AI-Generated Software Refactoring:
A Comparative Experimental Study Using Large Language Models
"""

import os

import matplotlib.pyplot as plt
import pandas as pd


# ==========================================================
# Configuration
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

METRICS_DIR = os.path.join(BASE_DIR, "metrics")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
GRAPH_DIR = os.path.join(BASE_DIR, "graphs")

AVERAGE_DIR = os.path.join(GRAPH_DIR, "average")
EXPERIMENT_DIR = os.path.join(GRAPH_DIR, "experiments")
DASHBOARD_DIR = os.path.join(GRAPH_DIR, "dashboard")
TABLE_DIR = os.path.join(GRAPH_DIR, "tables")

for directory in (
    GRAPH_DIR,
    AVERAGE_DIR,
    EXPERIMENT_DIR,
    DASHBOARD_DIR,
    TABLE_DIR,
):
    os.makedirs(directory, exist_ok=True)

SUMMARY_FILE = os.path.join(METRICS_DIR, "summary_results.csv")
AVERAGE_FILE = os.path.join(RESULTS_DIR, "average_metrics.csv")
WIN_FILE = os.path.join(RESULTS_DIR, "win_count.csv")
RANK_FILE = os.path.join(RESULTS_DIR, "overall_ranking.csv")


# ==========================================================
# Plot Style
# ==========================================================

plt.rcParams.update({
    "figure.figsize": (8, 5),
    "figure.dpi": 300,
    "axes.grid": True,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
})


# ==========================================================
# Load Data
# ==========================================================

summary_df = pd.read_csv(SUMMARY_FILE)
average_df = pd.read_csv(AVERAGE_FILE)
win_df = pd.read_csv(WIN_FILE)
rank_df = pd.read_csv(RANK_FILE)

print("Datasets loaded successfully.")
print(summary_df.columns.tolist())
# ==========================================================
# Helper Function
# ==========================================================

def save_figure(fig, folder, filename):
    """
    Save a matplotlib figure with consistent settings.
    """
    output_path = os.path.join(folder, filename)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {output_path}")


# ==========================================================
# Average Metric Graphs
# ==========================================================

def plot_average_metric(metric, ylabel, filename):
    """
    Generate a bar chart for an average metric.
    """

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        average_df["Model"],
        average_df[metric],
    )

    ax.set_title(f"Average {metric} by Model")
    ax.set_xlabel("Large Language Model")
    ax.set_ylabel(ylabel)

    save_figure(fig, AVERAGE_DIR, filename)


def plot_average_loc():
    plot_average_metric(
        metric="LOC",
        ylabel="Average Lines of Code",
        filename="average_loc.png",
    )


def plot_average_cc():
    plot_average_metric(
        metric="CC",
        ylabel="Average Cyclomatic Complexity",
        filename="average_cc.png",
    )


def plot_average_mi():
    plot_average_metric(
        metric="MI",
        ylabel="Average Maintainability Index",
        filename="average_mi.png",
    )


# ==========================================================
# Win Count
# ==========================================================

def plot_win_count():

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        win_df["Model"],
        win_df["Wins"],
    )

    ax.set_title("Experiment Wins")
    ax.set_xlabel("Large Language Model")
    ax.set_ylabel("Number of Wins")

    save_figure(
        fig,
        AVERAGE_DIR,
        "win_count.png",
    )


# ==========================================================
# Overall Ranking
# ==========================================================

def plot_average_rank():

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        rank_df["Model"],
        rank_df["Average Rank"],
    )

    ax.set_title("Average Ranking")
    ax.set_xlabel("Large Language Model")
    ax.set_ylabel("Average Rank")

    save_figure(
        fig,
        AVERAGE_DIR,
        "average_rank.png",
    )