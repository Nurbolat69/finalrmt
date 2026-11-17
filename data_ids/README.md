# Dataset Metadata, Provenance & Checksums

This directory documents data provenance, cryptographic checksums (SHA-256), and frozen sampling seeds for all benchmarks evaluated in:
> *Commercial and Open-Weight LLMs on Kazakh: Benchmarking Question Answering, Translation, and Summarization* (Nurbolat Suleimenov, 2026).

## Overview

| Task | Dataset | Source / Split | SHA-256 Checksum | Sample Size (n) | Seed |
|---|---|---|---|---|---|
| **Question Answering** | KazMMLU (Cyrillic) | HuggingFace `kz-transformers/kaz-mmlu` | `ddee2772628f82...` | 998 (stratified) | 42 |
| **Machine Translation (kk→en)** | FLORES-200 | `kaz_Cyrl.devtest` | `71e2301ba312fa...` | 1,012 sentence pairs | 42 |
| **Machine Translation (en→kk)** | FLORES-200 | `eng_Latn.devtest` | `612e9fbe879976...` | 1,012 sentence pairs | 42 |
| **Summarization** | KazSumm | Tengrinews.kz / `issai/kazSumm` test | `ddee2772628f82...` | 500 articles | 42 |

## Integrity & Licensing Notes
1. **KazMMLU:** 14 questions with defective or absent answer keys were removed prior to drawing the stratified sample of 998 questions across 12 subjects.
2. **FLORES-200:** Sentence pairs are evaluated deterministically in both directions under identical greedy decoding settings.
3. **KazSumm:** Articles originate from Tengrinews.kz with headline reference summaries (median 8 words). In accordance with intellectual property laws, full article texts are not redistributed. Identifiers and checksums allow verified local reproduction.
