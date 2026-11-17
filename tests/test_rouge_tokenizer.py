"""
tests/test_rouge_tokenizer.py
=============================
Unit tests verifying the Unicode-aware ROUGE tokenizer for Kazakh Cyrillic text.

Context:
The standard rouge_score DefaultTokenizer discards all non-Latin characters:
    re.sub(r"[^a-z0-9]+", " ", text.lower()).split()
which causes identical Cyrillic strings to be evaluated as empty strings and
return a ROUGE score of 0.0.
The UnicodeTokenizer implemented in code/utils.py preserves all Unicode word
characters, guaranteeing proper evaluation of Kazakh text.

These 7 unit tests rigorously verify:
1. Identical Kazakh Cyrillic sentences score 1.0 (vs 0.0 with default tokenizer)
2. Cyrillic text with digits/years scores 1.0
3. Case-insensitivity across uppercase and lowercase Cyrillic characters
4. Preservation of all 9 Kazakh-specific letters (ә, і, ң, ғ, ү, ұ, қ, ө, һ)
5. Predictable partial overlap scoring (LCS precision / recall / F1)
6. Robust stripping of Cyrillic punctuation (« », —, commas, quotes)
7. Completely disjoint Kazakh sentences score 0.0
"""

import sys
from pathlib import Path
import pytest
import re

# Add code/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))
from utils import UnicodeTokenizer


def compute_rouge_l_single(ref: str, hyp: str, tokenizer=None) -> float:
    """Helper to compute single-item ROUGE-L F1 with a given tokenizer."""
    try:
        from rouge_score import rouge_scorer
        tok = tokenizer or UnicodeTokenizer()
        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False, tokenizer=tok)
        return scorer.score(ref, hyp)["rougeL"].fmeasure
    except ImportError:
        # Standalone fallback if rouge_score is not installed in the active environment
        tok = tokenizer or UnicodeTokenizer()
        ref_tokens = tok.tokenize(ref)
        hyp_tokens = tok.tokenize(hyp)
        if not ref_tokens or not hyp_tokens:
            return 0.0
        # Compute LCS
        m, n = len(ref_tokens), len(hyp_tokens)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                if ref_tokens[i] == hyp_tokens[j]:
                    dp[i + 1][j + 1] = dp[i][j] + 1
                else:
                    dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])
        lcs = dp[m][n]
        prec = lcs / n
        rec = lcs / m
        if prec + rec == 0:
            return 0.0
        return (2 * prec * rec) / (prec + rec)


def test_1_cyrillic_identical_string_scores_one():
    """Test 1: Identical Kazakh Cyrillic sentence must score 1.0."""
    text = "Қазақстанның астанасы Астана қаласы"
    tokenizer = UnicodeTokenizer()
    tokens = tokenizer.tokenize(text)
    assert len(tokens) == 4, f"Expected 4 tokens, got {tokens}"
    score = compute_rouge_l_single(text, text, tokenizer=tokenizer)
    assert score == pytest.approx(1.0, rel=1e-5), f"Expected 1.0, got {score}"


def test_2_cyrillic_with_numbers_scores_one():
    """Test 2: Kazakh sentence containing dates and numbers must score 1.0."""
    text = "2026 жылы 17 қараша күні емтихан өтеді"
    tokenizer = UnicodeTokenizer()
    score = compute_rouge_l_single(text, text, tokenizer=tokenizer)
    assert score == pytest.approx(1.0, rel=1e-5), f"Expected 1.0, got {score}"


def test_3_cyrillic_case_insensitivity():
    """Test 3: Tokenizer must be case-insensitive for Kazakh Cyrillic."""
    ref = "АСТАНА ҚАЛАСЫ"
    hyp = "астана қаласы"
    tokenizer = UnicodeTokenizer()
    score = compute_rouge_l_single(ref, hyp, tokenizer=tokenizer)
    assert score == pytest.approx(1.0, rel=1e-5), f"Expected 1.0, got {score}"


def test_4_kazakh_specific_characters_preserved():
    """Test 4: All Kazakh-specific alphabet characters (ә, і, ң, ғ, ү, ұ, қ, ө, һ) must be preserved."""
    kazakh_alphabet_sample = "әке іні қарындас оңтүстік ұлт ғалым өнер һәріп"
    tokenizer = UnicodeTokenizer()
    tokens = tokenizer.tokenize(kazakh_alphabet_sample)
    expected_count = 8
    assert len(tokens) == expected_count, f"Expected {expected_count} tokens, got {tokens}"
    score = compute_rouge_l_single(kazakh_alphabet_sample, kazakh_alphabet_sample, tokenizer=tokenizer)
    assert score == pytest.approx(1.0, rel=1e-5), f"Expected 1.0, got {score}"


def test_5_cyrillic_partial_overlap():
    """Test 5: Partial overlap computes exact expected ROUGE-L F1."""
    ref = "Астана әдемі әрі заманауи қала"      # 5 tokens
    hyp = "Астана үлкен әрі заманауи қала"      # 5 tokens, 4 common in sequence
    tokenizer = UnicodeTokenizer()
    # LCS is ['астана', 'әрі', 'заманауи', 'қала'] = 4 tokens
    # P = 4/5, R = 4/5 -> F1 = 0.8
    score = compute_rouge_l_single(ref, hyp, tokenizer=tokenizer)
    assert score == pytest.approx(0.8, rel=1e-5), f"Expected 0.8, got {score}"


def test_6_cyrillic_punctuation_stripping():
    """Test 6: Punctuation marks (« », —, commas, quotes, dashes) are stripped without modifying tokens."""
    ref = "«Сәлем, әлем!» — деп айтты."
    hyp = "Сәлем әлем деп айтты"
    tokenizer = UnicodeTokenizer()
    score = compute_rouge_l_single(ref, hyp, tokenizer=tokenizer)
    assert score == pytest.approx(1.0, rel=1e-5), f"Expected 1.0, got {score}"


def test_7_cyrillic_disjoint_strings_scores_zero():
    """Test 7: Completely disjoint Kazakh sentences must score 0.0."""
    ref = "Бүгін ауа райы ашық және жылы болады"
    hyp = "Кітапханада жаңа кітаптар көрмесі ашылды"
    tokenizer = UnicodeTokenizer()
    score = compute_rouge_l_single(ref, hyp, tokenizer=tokenizer)
    assert score == pytest.approx(0.0, abs=1e-5), f"Expected 0.0, got {score}"
