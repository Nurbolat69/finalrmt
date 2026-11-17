"""
code/gaps.py
============
Reproduces Table 5 from the manuscript:
"Commercial–open-weight gap and the performance gain associated with Kazakh adaptation"

Exports results/table5.csv.

Usage:
    python code/gaps.py
"""

from pathlib import Path
import csv

def main():
    root = Path(__file__).resolve().parent.parent
    out_dir = root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "table5.csv"

    # Data from Table 3 model means:
    # GPT-4o and Gemini 1.5 Pro mean vs Llama-3.1-8B and Sherkala-Chat 8B
    items = [
        {
            "task": "QA (accuracy)",
            "comm_mean": 70.15,
            "llama": 41.3,
            "sherkala": 46.8,
        },
        {
            "task": "MT kk->en (chrF++)",
            "comm_mean": 61.55,
            "llama": 38.6,
            "sherkala": 44.2,
        },
        {
            "task": "MT en->kk (chrF++)",
            "comm_mean": 53.05,
            "llama": 29.4,
            "sherkala": 36.1,
        },
        {
            "task": "Summarization (ROUGE-L)",
            "comm_mean": 30.50,
            "llama": 22.1,
            "sherkala": 25.9,
        },
        {
            "task": "Summarization (chrF++)",
            "comm_mean": 37.65,
            "llama": 27.3,
            "sherkala": 31.7,
        },
    ]

    headers = [
        "Task (metric)",
        "Commercial mean",
        "Llama",
        "Absolute gap",
        "Relative gap (%)",
        "Sherkala - Llama",
        "Gap closed (%)",
    ]

    rows = []
    print("=" * 95)
    print("TABLE 5: Commercial–Open-Weight Gap and Share Closed by Kazakh Adaptation")
    print("=" * 95)
    print(f"{'Task (metric)':<25} | {'Comm Mean':<10} | {'Llama':<7} | {'Abs Gap':<9} | {'Rel Gap (%)':<12} | {'Sherkala-Llama':<15} | {'Gap Closed (%)':<14}")
    print("-" * 95)

    for item in items:
        abs_gap = round(item["comm_mean"] - item["llama"], 1)
        rel_gap = round((item["comm_mean"] - item["llama"]) / item["comm_mean"] * 100, 1)
        sherk_diff = round(item["sherkala"] - item["llama"], 1)
        closed_pct = round((item["sherkala"] - item["llama"]) / (item["comm_mean"] - item["llama"]) * 100, 1)

        row = [
            item["task"],
            f"{item['comm_mean']:.2f}",
            f"{item['llama']:.1f}",
            f"{abs_gap:.1f}",
            f"{rel_gap:.1f}",
            f"+{sherk_diff:.1f}",
            f"{closed_pct:.1f}",
        ]
        rows.append(row)
        print(f"{item['task']:<25} | {item['comm_mean']:>9.2f}  | {item['llama']:>5.1f} | {abs_gap:>7.1f} | {rel_gap:>10.1f}% | {('+' + str(sherk_diff)):>14} | {closed_pct:>13.1f}%")

    print("-" * 95)
    print("Relative gap = (commercial mean - Llama) / commercial mean * 100")
    print("Gap closed   = (Sherkala - Llama) / (commercial mean - Llama) * 100")

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Successfully generated: {out_file}\n")

if __name__ == "__main__":
    main()
