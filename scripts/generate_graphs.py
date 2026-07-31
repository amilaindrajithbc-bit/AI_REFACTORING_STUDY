"""
Generate publication-quality graphs for the AI Refactoring Study.

Author: Amila Piyasiri
"""

import os

import matplotlib.pyplot as plt
import pandas as pd


# ==========================================================
# Project Directories
# ==========================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

METRICS_DIR = os.path.join(PROJECT_ROOT, "metrics")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

GRAPHS_DIR = os.path.join(PROJECT_ROOT, "graphs")

AVERAGE_DIR = os.path.join(GRAPHS_DIR, "average")
EXPERIMENTS_DIR = os.path.join(GRAPHS_DIR, "experiments")
DASHBOARD_DIR = os.path.join(GRAPHS_DIR, "dashboard")
TABLES_DIR = os.path.join(GRAPHS_DIR, "tables")

for directory in (
    GRAPHS_DIR,
    AVERAGE_DIR,
    EXPERIMENTS_DIR,
    DASHBOARD_DIR,
    TABLES_DIR,
):
    os.makedirs(directory, exist_ok=True)


# ==========================================================
# Input Files
# ==========================================================

SUMMARY_RESULTS = os.path.join(METRICS_DIR, "summary_results.csv")
AVERAGE_METRICS = os.path.join(RESULTS_DIR, "average_metrics.csv")
WIN_COUNT = os.path.join(RESULTS_DIR, "win_count.csv")
OVERALL_RANKING = os.path.join(RESULTS_DIR, "overall_ranking.csv")


# ==========================================================
# Load Data
# ==========================================================

summary_df = pd.read_csv(SUMMARY_RESULTS)
average_df = pd.read_csv(AVERAGE_METRICS)
win_df = pd.read_csv(WIN_COUNT)
ranking_df = pd.read_csv(OVERALL_RANKING)

print("Datasets loaded successfully.")


# ==========================================================
# Matplotlib Settings
# ==========================================================

plt.style.use("ggplot")

plt.rcParams["figure.figsize"] = (8, 5)
plt.rcParams["figure.dpi"] = 300

plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12

plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10

plt.rcParams["legend.fontsize"] = 10


# ==========================================================
# Helper Function
# ==========================================================

def save_figure(filename):
    """Save and close current figure."""
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()


# ==========================================================
# Average Metric Graphs
# ==========================================================

def plot_loc():
    plt.figure()

    plt.bar(
        average_df["Model"],
        average_df["LOC"],
    )

    plt.title("Average Lines of Code (LOC)")
    plt.xlabel("Model")
    plt.ylabel("LOC")

    save_figure(
        os.path.join(
            AVERAGE_DIR,
            "loc_comparison.png",
        )
    )


def plot_cc():
    plt.figure()

    plt.bar(
        average_df["Model"],
        average_df["CC"],
    )

    plt.title("Average Cyclomatic Complexity")
    plt.xlabel("Model")
    plt.ylabel("CC")

    save_figure(
        os.path.join(
            AVERAGE_DIR,
            "cc_comparison.png",
        )
    )


def plot_mi():
    plt.figure()

    plt.bar(
        average_df["Model"],
        average_df["MI"],
    )

    plt.title("Average Maintainability Index")
    plt.xlabel("Model")
    plt.ylabel("MI")

    save_figure(
        os.path.join(
            AVERAGE_DIR,
            "mi_comparison.png",
        )
    )
# ==========================================================
# Win Count Graph
# ==========================================================

def plot_win_count():
    """Generate win count comparison graph."""

    plt.figure()

    bars = plt.bar(
        win_df["Model"],
        win_df["Wins"],
    )

    plt.title("Win Count by Model")
    plt.xlabel("Model")
    plt.ylabel("Wins")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
        )

    save_figure(
        os.path.join(
            AVERAGE_DIR,
            "win_count.png",
        )
    )


# ==========================================================
# Average Rank Graph
# ==========================================================

def plot_average_rank():
    """Generate average ranking graph."""

    plt.figure()

    bars = plt.bar(
        ranking_df["Model"],
        ranking_df["Average Rank"],
    )

    plt.title("Average Rank")
    plt.xlabel("Model")
    plt.ylabel("Average Rank")

    # Smaller rank is better
    plt.gca().invert_yaxis()

    for bar in bars:
        value = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"{value:.2f}",
            ha="center",
            va="bottom",
        )

    save_figure(
        os.path.join(
            AVERAGE_DIR,
            "average_rank.png",
        )
    )


# ==========================================================
# Summary Tables
# ==========================================================

def dataframe_to_image(df, title, output_file):
    """
    Save a pandas DataFrame as a PNG table.
    """

    fig, ax = plt.subplots(
        figsize=(8, len(df) * 0.6 + 1.5)
    )

    ax.axis("off")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    plt.title(title)

    save_figure(output_file)


def create_tables():

    dataframe_to_image(
        average_df,
        "Average Metrics",
        os.path.join(
            TABLES_DIR,
            "average_metrics_table.png",
        ),
    )

    dataframe_to_image(
        win_df,
        "Win Count",
        os.path.join(
            TABLES_DIR,
            "win_count_table.png",
        ),
    )

    dataframe_to_image(
        ranking_df,
        "Overall Ranking",
        os.path.join(
            TABLES_DIR,
            "ranking_table.png",
        ),
    )


# ==========================================================
# Experiment-wise Graphs
# ==========================================================

def plot_single_experiment(exp_df, experiment_no):
    """
    Generate LOC, CC and MI comparison graph
    for a single experiment.
    """

    # Remove Original
    ai_df = exp_df[exp_df["Model"] != "Original"]

    metrics = ["LOC", "CC", "MI"]

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(15, 5)
    )

    for ax, metric in zip(axes, metrics):

        bars = ax.bar(
            ai_df["Model"],
            ai_df[metric],
        )

        ax.set_title(metric)
        ax.set_xlabel("Model")
        ax.set_ylabel(metric)

        for bar in bars:

            value = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value,
                f"{value:.2f}" if metric == "MI" else f"{int(value)}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    repository = exp_df.iloc[0]["Repository"]
    function = exp_df.iloc[0]["Function"]

    plt.suptitle(
        f"Experiment {experiment_no}\n"
        f"{repository} : {function}",
        fontsize=14,
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            EXPERIMENTS_DIR,
            f"experiment_{experiment_no:02d}.png",
        ),
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


# ==========================================================
# Repository Comparison
# ==========================================================

def plot_repository_mi():

    ai_df = summary_df[
        summary_df["Model"] != "Original"
    ]

    pivot = ai_df.pivot(
        index="Repository",
        columns="Model",
        values="MI",
    )

    pivot.plot(
        kind="bar",
        figsize=(10, 6),
    )

    plt.title("Maintainability Index by Repository")

    plt.xlabel("Repository")
    plt.ylabel("MI")

    plt.legend(title="Model")

    save_figure(
        os.path.join(
            EXPERIMENTS_DIR,
            "repository_mi.png",
        )
    )


def plot_repository_loc():

    ai_df = summary_df[
        summary_df["Model"] != "Original"
    ]

    pivot = ai_df.pivot(
        index="Repository",
        columns="Model",
        values="LOC",
    )

    pivot.plot(
        kind="bar",
        figsize=(10, 6),
    )

    plt.title("Lines of Code by Repository")

    plt.xlabel("Repository")
    plt.ylabel("LOC")

    plt.legend(title="Model")

    save_figure(
        os.path.join(
            EXPERIMENTS_DIR,
            "repository_loc.png",
        )
    )


def plot_repository_cc():

    ai_df = summary_df[
        summary_df["Model"] != "Original"
    ]

    pivot = ai_df.pivot(
        index="Repository",
        columns="Model",
        values="CC",
    )

    pivot.plot(
        kind="bar",
        figsize=(10, 6),
    )

    plt.title("Cyclomatic Complexity by Repository")

    plt.xlabel("Repository")
    plt.ylabel("CC")

    plt.legend(title="Model")

    save_figure(
        os.path.join(
            EXPERIMENTS_DIR,
            "repository_cc.png",
        )
    )


# ==========================================================
# Create Experiment Graphs
# ==========================================================

def create_experiment_graphs():

    experiments = sorted(
        summary_df["Experiment"].unique()
    )

    for experiment in experiments:

        exp_df = summary_df[
            summary_df["Experiment"] == experiment
        ]

        plot_single_experiment(
            exp_df,
            experiment,
        )

    plot_repository_loc()

    plot_repository_cc()

    plot_repository_mi()

    print(
        f"{len(experiments)} experiment graphs generated."
    ) 
# ==========================================================
# Dashboard
# ==========================================================

def create_dashboard():
    """
    Create a dashboard containing the
    three average metric comparisons.
    """

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(18, 6)
    )

    metrics = ["LOC", "CC", "MI"]

    for ax, metric in zip(axes, metrics):

        bars = ax.bar(
            average_df["Model"],
            average_df[metric],
        )

        ax.set_title(metric)
        ax.set_xlabel("Model")
        ax.set_ylabel(metric)

        for bar in bars:

            value = bar.get_height()

            if metric == "MI":
                label = f"{value:.2f}"
            else:
                label = f"{value:.1f}"

            ax.text(
                bar.get_x() + bar.get_width()/2,
                value,
                label,
                ha="center",
                va="bottom",
                fontsize=8,
            )

    plt.suptitle(
        "Overall AI Refactoring Performance",
        fontsize=16,
    )

    save_figure(
        os.path.join(
            DASHBOARD_DIR,
            "overall_dashboard.png",
        )
    )


# ==========================================================
# Model Summary
# ==========================================================

def create_model_summary():

    summary = average_df.copy()

    summary["Wins"] = win_df["Wins"]

    summary["Average Rank"] = ranking_df["Average Rank"]

    dataframe_to_image(
        summary,
        "Model Summary",
        os.path.join(
            TABLES_DIR,
            "model_summary.png",
        ),
    )


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("Generating Graphs")
    print("=" * 60)

    plot_loc()
    plot_cc()
    plot_mi()

    plot_win_count()
    plot_average_rank()

    create_tables()

    create_experiment_graphs()

    create_dashboard()

    create_model_summary()

    print()
    print("=" * 60)
    print("Completed Successfully")
    print("=" * 60)

    print()

    print("Output folders")

    print(f"Average     : {AVERAGE_DIR}")
    print(f"Experiments : {EXPERIMENTS_DIR}")
    print(f"Dashboard   : {DASHBOARD_DIR}")
    print(f"Tables      : {TABLES_DIR}")

    print()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()    