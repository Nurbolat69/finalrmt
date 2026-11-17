"""
code/figures.py
===============
Generates high-resolution figures (Fig. 1 and Fig. 2) matching the manuscript:
  - Fig. 1: Primary metric performance by model and task (with 95% bootstrap CIs)
  - Fig. 2: Commercial mean-Llama relative gap by task and share closed by Sherkala

Usage:
    python code/figures.py
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def main():
    root = Path(__file__).resolve().parent.parent
    figures_dir = root / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Style configuration
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    plt.rcParams["axes.edgecolor"] = "#333333"
    plt.rcParams["axes.linewidth"] = 0.8

    # -------------------------------------------------------------
    # Figure 1: Main Results by Task & Condition (Panels a, b, c)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.2), sharey=False)

    model_labels = ["Baseline", "Llama 3.1", "Sherkala", "GPT-4o", "Gemini 1.5"]
    primary_color = "#1f77b4"

    # (a) KazMMLU QA Accuracy (%)
    qa_means = [23.5, 41.3, 46.8, 71.4, 68.9]
    qa_err_low = [23.5 - 21.0, 41.3 - 38.2, 46.8 - 43.7, 71.4 - 68.5, 68.9 - 66.0]
    qa_err_high = [26.1 - 23.5, 44.4 - 41.3, 50.0 - 46.8, 74.2 - 71.4, 71.8 - 68.9]

    axes[0].bar(model_labels, qa_means, yerr=[qa_err_low, qa_err_high], capsize=5, color=primary_color, edgecolor="#0e4166", width=0.7)
    axes[0].set_title("(a) KazMMLU question answering", fontsize=13, pad=10)
    axes[0].set_ylabel("Accuracy (%)", fontsize=11)
    axes[0].set_ylim(0, 85)
    axes[0].tick_params(axis="x", rotation=15, labelsize=10)

    # (b) FLORES-200 kk->en chrF++
    mt_means = [7.1, 38.6, 44.2, 62.8, 60.3]
    mt_err_low = [7.1 - 6.4, 38.6 - 37.0, 44.2 - 42.5, 62.8 - 61.2, 60.3 - 58.6]
    mt_err_high = [7.9 - 7.1, 40.2 - 38.6, 45.9 - 44.2, 64.4 - 62.8, 61.9 - 60.3]

    axes[1].bar(model_labels, mt_means, yerr=[mt_err_low, mt_err_high], capsize=5, color=primary_color, edgecolor="#0e4166", width=0.7)
    axes[1].set_title("(b) FLORES-200 kk→en translation", fontsize=13, pad=10)
    axes[1].set_ylabel("chrF++", fontsize=11)
    axes[1].set_ylim(0, 75)
    axes[1].tick_params(axis="x", rotation=15, labelsize=10)

    # (c) KazSumm Summarization ROUGE-L
    summ_means = [18.4, 22.1, 25.9, 31.2, 29.8]
    summ_err_low = [18.4 - 17.2, 22.1 - 20.6, 25.9 - 24.3, 31.2 - 29.5, 29.8 - 28.1]
    summ_err_high = [19.6 - 18.4, 23.6 - 22.1, 27.4 - 25.9, 32.8 - 31.2, 31.4 - 29.8]

    axes[2].bar(model_labels, summ_means, yerr=[summ_err_low, summ_err_high], capsize=5, color=primary_color, edgecolor="#0e4166", width=0.7)
    axes[2].set_title("(c) KazSumm summarization", fontsize=13, pad=10)
    axes[2].set_ylabel("ROUGE-L", fontsize=11)
    axes[2].set_ylim(0, 40)
    axes[2].tick_params(axis="x", rotation=15, labelsize=10)

    plt.tight_layout()
    fig1_path = figures_dir / "fig1_main_results.png"
    plt.savefig(fig1_path, dpi=300)
    print(f"Generated: {fig1_path}")
    plt.close()

    # -------------------------------------------------------------
    # Figure 2: Commercial mean-Llama relative gap by task
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 4.5))
    tasks = ["QA", "MT kk→en", "MT en→kk", "Summarization"]
    rel_gaps = [41.1, 37.3, 44.6, 27.5]

    bars = ax.bar(tasks, rel_gaps, color="#1f77b4", width=0.6, edgecolor="#0e4166")
    ax.set_title("Commercial mean–Llama relative gap by task", fontsize=13, pad=12)
    ax.set_ylabel("Relative gap (%)", fontsize=11)
    ax.set_ylim(0, 52)

    for bar, val in zip(bars, rel_gaps):
        height = bar.get_height()
        ax.annotate(f"{val:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center", va="bottom",
                    fontweight="bold", fontsize=10)

    plt.tight_layout()
    fig2_path = figures_dir / "fig2_gap_across_tasks.png"
    plt.savefig(fig2_path, dpi=300)
    print(f"Generated: {fig2_path}")
    plt.close()

if __name__ == "__main__":
    main()
