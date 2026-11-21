import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from normalization.normalize import normalize_arabic
from rag.search import search

DATA = Path(__file__).parent / "retrieval.jsonl"

def _norm(s):
    return normalize_arabic(s).casefold()

def load_examples():
    with open(DATA, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def run(k=3):
    examples = load_examples()
    hit1 = hit3 = 0
    for i, ex in enumerate(examples, start=1):
        results = search(ex["question"], k=k)
        titles = [r["title"] for r in results]
       
        rank = next(
            (n for n, t in enumerate(titles, start=1) if _norm(ex["expected"]) in _norm(t)),
            None,
        )
        hit1 += rank == 1
        hit3 += rank is not None
        print(f"{i:02d} rank={rank}  top_ids={[r['id'] for r in results]}")
    n = len(examples)
    print(f"\nHit@1: {hit1}/{n} = {hit1 / n:.0%}")
    print(f"Hit@{k}: {hit3}/{n} = {hit3 / n:.0%}")

if __name__ == "__main__":
    run()
