# finalrmt — Benchmark Evaluation & Reproducibility Package

Reproducibility repository for the final benchmark evaluation.
Release tag: `final`.

## Repository Structure

- `code/`: Execution, evaluation, and reproduction scripts
  - `make_table3.py`: Generates master results table (`results/table3.csv`)
  - `paired_tests.py`: Computes Holm-corrected paired tests (`results/table4.csv`)
  - `gaps.py`: Calculates performance gaps and adaptation closure (`results/table5.csv`)
  - `by_subject.py`: Computes QA subject breakdown (`results/table6.csv`)
  - `error_counts.py`: Generates qualitative error categorization (`results/table7.csv`)
  - `figures.py`: Generates benchmark figures (`figures/`)
  - `utils.py`: Bootstrap CI, Holm correction, and Unicode-aware ROUGE tokenizer
  - `run_qa.py`, `run_mt.py`, `run_summ.py`: Evaluation runners
- `prompts/`: Exact zero-shot prompt templates for QA, MT, and summarization
- `data_ids/`: Dataset identifiers, sampling seeds (42), and SHA-256 hashes
- `outputs/`: Pre-computed evaluation logs and test records
- `logs/`: Task run logs (`qa_run_log.json`, `mt_run_log.json`, `summ_run_log.json`)
- `results/`: Pre-generated CSV tables for all manuscript results
- `figures/`: Figure scripts and visual assets
- `tests/`: Unit test suite (verifies Unicode-aware ROUGE tokenizer)
- `requirements.txt` / `environment.yml`: Pinned dependency configurations
- `LICENSE`: MIT License

## Environment & Hardware

- Python: 3.12
- Pinned libraries: `requirements.txt` / `environment.yml`
- Local models: NVIDIA A100 GPU (80 GB), batch size 1, bfloat16 precision
- API models: `gpt-4o-2024-11-20`, `gemini-1.5-pro-002` (via environment variables)

## Results Reproduction

Run each script from the repository root:

| Target Item | Command | Output File |
|---|---|---|
| Table 3 (Main results + CIs) | `python code/make_table3.py` | `results/table3.csv` |
| Table 4 (Holm-corrected tests) | `python code/paired_tests.py` | `results/table4.csv` |
| Table 5 (Task gaps & closure) | `python code/gaps.py` | `results/table5.csv` |
| Table 6 (QA by subject) | `python code/by_subject.py` | `results/table6.csv` |
| Table 7 (Error categories) | `python code/error_counts.py` | `results/table7.csv` |
| Figures 1 & 2 | `python code/figures.py` | `figures/` |

## Unit Tests

Run the test suite with pytest:
```bash
pytest tests/
```
Includes 7 unit tests verifying that the Unicode-aware ROUGE tokenizer handles Cyrillic characters properly (scoring 1.0 on identical strings).

## Data & License

- Code: MIT License
- Benchmarks: Public benchmarks (KazMMLU, FLORES-200, KazSumm) under original licenses
- KazSumm article texts are copyrighted by Tengrinews.kz and are not redistributed; dataset IDs and hashes are provided in `data_ids/`.
