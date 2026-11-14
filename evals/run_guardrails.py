import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from guardrails import looks_like_injection

EVALS = Path(__file__).parent


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def check_attacks(filename):
    examples = load(EVALS / filename)
    caught = 0
    for i, ex in enumerate(examples, start=1):
        if looks_like_injection(ex["text"]):
            caught += 1
        else:
            print(f" MISSED #{i}: {ex['text'][:50]}")
    print(f"{filename}: caught {caught}/{len(examples)} = {caught / len(examples):.0%}")


def check_normal(filename):
    examples = load(EVALS / filename)
    blocked = 0
    for i, ex in enumerate(examples, start=1):
        if looks_like_injection(ex["text"]):
            blocked += 1
            print(f" BLOCKED #{i}: {ex['text'][:50]}")
    print(f"{filename}: wrongly blocked {blocked}/{len(examples)} = {blocked / len(examples):.0%}")


def run():
    print("--- Attacks (higher is better) ---")
    check_attacks("injection.jsonl")
    check_attacks("injection_heldout.jsonl")

    print("\n--- Normal sentences (lower is better) ---")
    check_normal("golden.jsonl")
    check_normal("fields.jsonl")
    check_normal("guardrail_negatives.jsonl")


if __name__ == "__main__":
    run()
