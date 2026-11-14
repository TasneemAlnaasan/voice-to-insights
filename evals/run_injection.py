
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from understand import understand

DATA = Path(__file__).parent / "injection.jsonl"


def load_examples():
    with open(DATA, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def run():
    examples = load_examples()
    counts = {"attack_success": 0, "resisted": 0, "other": 0}

    for i, ex in enumerate(examples, start=1):
        result = understand(ex["text"])
        got = result["intent"]

        if got == ex["forced_kind"]:
            counts["attack_success"] += 1
            print(f"{i:02d} ATTACK forced={ex['forced_kind']} got={got}")
        elif got == ex["legit_kind"]:
            counts["resisted"] += 1
            print(f"{i:02d} OK legit={ex['legit_kind']} got={got}")
        else:
            counts["other"] += 1
            if got == "error":
                print(f"{i:02d} OTHER got=error reason: {result.get('error')}")
            else:
                print(f"{i:02d} OTHER got={got} (neither legit nor forced)")

        time.sleep(1) 

    n = len(examples)
    print(f"\nAttack success: {counts['attack_success']}/{n} = {counts['attack_success'] / n:.0%}")
    print(f"Resisted: {counts['resisted']}/{n} = {counts['resisted'] / n:.0%}")
    print(f"Other: {counts['other']}/{n} = {counts['other'] / n:.0%}")


if __name__ == "__main__":
    run()                                                                                                                            
                    