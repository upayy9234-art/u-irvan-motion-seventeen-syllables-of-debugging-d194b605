#!/usr/bin/env python3
"""Seventeen Syllables of Debugging.

Prints one haiku about debugging: exactly 17 syllables in a 5-7-5
pattern, three lines, the same fixed string on every run.

The program holds a few candidate haikus, scores each one against the
brief (correct 5-7-5 counts, about debugging, fresh, readable) and
prints the winner. Pure standard library, fully deterministic.
"""

import os
import re

CANDIDATES = [
    (
        "Code breaks at midnight",
        "one missed semicolon hides",
        "morning brings the fix",
    ),
    (
        "Red tests blink at dawn",
        "one stray print reveals the flaw",
        "green lights return home",
    ),
    (
        "The log stays silent",
        "a typo sleeps in plain sight",
        "patience finds the bug",
    ),
]

DEBUG_WORDS = {
    "code", "bug", "test", "tests", "log", "print", "typo",
    "semicolon", "flaw", "fix", "debug", "debugging",
}


def count_syllables(word):
    """Count syllables in one English word (heuristic, stdlib only)."""
    word = word.lower().strip(".,;:!?\"'")
    if not word:
        return 0
    # Common irregulars that the generic rule gets wrong.
    irregular = {
        "code": 1, "breaks": 1, "midnight": 2, "missed": 1,
        "semicolon": 4, "hides": 1, "morning": 2, "brings": 1,
        "fix": 1, "silent": 2, "typo": 2, "sleeps": 1, "plain": 1,
        "sight": 1, "patience": 2, "finds": 1, "bug": 1,
        "blink": 1, "dawn": 1, "stray": 1, "print": 1, "reveals": 2,
        "flaw": 1, "green": 1, "lights": 1, "return": 2, "home": 1,
        "red": 1, "tests": 1, "one": 1, "the": 1, "at": 1, "a": 1,
        "in": 1,
    }
    if word in irregular:
        return irregular[word]
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    if word.endswith("ed") and count > 1 and not word.endswith("ted"):
        count -= 1
    return max(count, 1)


def line_syllables(line):
    """Total syllables in one line of the haiku."""
    return sum(count_syllables(w) for w in re.split(r"\s+", line.strip()))


def score_candidate(candidate):
    """Score a candidate haiku against the brief; higher is better."""
    counts = [line_syllables(line) for line in candidate]
    target = (5, 7, 5)
    score = 0
    for got, want in zip(counts, target):
        score -= abs(got - want) * 10
    if counts == list(target):
        score += 50
    text = " ".join(candidate).lower()
    words = set(re.findall(r"[a-z]+", text))
    score += 5 * len(words & DEBUG_WORDS)
    score += len(set(words))  # reward varied, readable wording
    return score


def pick_winner():
    """Pick the best-scoring candidate (first wins ties: deterministic)."""
    best = None
    best_score = None
    for candidate in CANDIDATES:
        score = score_candidate(candidate)
        if best_score is None or score > best_score:
            best, best_score = candidate, score
    return best


def main():
    haiku = pick_winner()
    text = "\n".join(haiku)
    print(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "entry.txt"), "w") as fh:
            fh.write(text + "\n")
    except OSError:
        pass  # stdout is the deliverable; the file copy is a bonus
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
