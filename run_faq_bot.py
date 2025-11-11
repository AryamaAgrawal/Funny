#!/usr/bin/env python3
"""
run_faq_bot.py
Simple offline FAQ bot that uses Copilot-generated KB (expanded_faq.json).
No external libraries required.

Usage:
    python run_faq_bot.py
"""

import json
import re
import math
import textwrap
from pathlib import Path
from collections import Counter

KB_PATH = Path("knowledge/expanded_faq.json")

def normalize(s):
    s = s.lower().strip()
    # remove punctuation
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s

def tokenize(s):
    return [t for t in normalize(s).split() if t]

def score_overlap(q_tokens, variant):
    v_tokens = tokenize(variant)
    if not v_tokens:
        return 0.0
    inter = len(set(q_tokens) & set(v_tokens))
    # simple score normalized by variant length
    return inter / math.sqrt(len(v_tokens))

def load_kb(path):
    if not path.exists():
        print(f"KB file not found: {path}")
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def find_best_entry(kb, query):
    q_tokens = tokenize(query)
    best = None
    best_score = 0.0
    for entry in kb:
        for qv in entry.get("question_variants", []):
            sc = score_overlap(q_tokens, qv)
            if sc > best_score:
                best_score = sc
                best = (entry, qv, sc)
    return best, best_score

def choose_answer(entry):
    variants = entry.get("answer_variants", [])
    if not variants:
        return "I'm sorry, I don't have an answer for that."
    # pick the shortest variant (concise) — could randomize to add variety
    variants_sorted = sorted(variants, key=lambda x: (len(x), x))
    return variants_sorted[0]

def interactive_loop(kb):
    print("FAQ Bot (Copilot KB). Type 'exit' to quit.")
    while True:
        try:
            q = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break
        if not q:
            continue
        if q.lower() in ("exit", "quit"):
            print("Goodbye.")
            break
        result, score = find_best_entry(kb, q)
        if result and score > 0:
            entry, matched_variant, sc = result
            ans = choose_answer(entry)
            print(f"\n[Answer — source: {entry.get('source', 'local')} | match={sc:.2f}]\n")
            print(textwrap.fill(ans, width=78))
            print()
        else:
            print("I don't have a direct answer in my offline KB for that question.")
            print("Try rephrasing, or ask about: mutual fund, compound interest, EMI, credit score, budgeting.")
            print()

def main():
    kb = load_kb(KB_PATH)
    if not kb:
        print("No KB loaded. Make sure knowledge/expanded_faq.json exists.")
        return
    print(f"Loaded {len(kb)} FAQ entries from {KB_PATH}")
    interactive_loop(kb)

if __name__ == "__main__":
    main()
