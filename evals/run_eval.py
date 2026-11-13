import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from understand import understand

DATA = Path(__file__).parent / "golden.jsonl"


def load_examples():
    with open(DATA, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def run():
    examples = load_examples()
    correct = 0
    for i, ex in enumerate(examples, start=1):
        result = understand(ex["text"])
        got = result["intent"]
        ok = got == ex["expected_kind"]
        correct += ok
        mark = "PASS" if ok else "FAIL"
        print(f"{i:02d} {mark} expected={ex['expected_kind']} got={got}")
        time.sleep(1)
    print(f"\nAccuracy: {correct}/{len(examples)} = {correct / len(examples):.0%}")


if __name__ == "__main__":
    run()
