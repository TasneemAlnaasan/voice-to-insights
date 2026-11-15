import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv 
load_dotenv(ROOT / ".env")

from understand import understand
from normalization.normalize import same_name

DATA = Path(__file__).parent / "fields.jsonl"


def load_examples():
    with open(DATA, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def run():
    examples = load_examples()
    scores = {"owner": 0, "priority": 0, "due_date": 0}
    is_task = 0

    for i, ex in enumerate(examples, start=1):
        result = understand(ex["text"])
        if result["intent"] == "error" and "429" in str(result.get("error")):
            print("Rate limit reached, stopping. Try again later.")
            print(result.get("error"))
            break
        data = result.get("data", {})

        task_ok = result["intent"] == "task"
        owner_ok = same_name(data.get("owner"), ex["owner"])
        priority_ok = data.get("priority") == ex["priority"]
        due_ok = (data.get("due_date") is not None) == ex["has_due_date"]

        is_task += task_ok
        scores["owner"] += owner_ok
        scores["priority"] += priority_ok
        scores["due_date"] += due_ok

        print(
            f"{i:02d} task={task_ok} owner={owner_ok} "
            f"priority={priority_ok} due={due_ok}"
        )
        if not owner_ok:
            print(f"   owner expected={ex['owner']!r} got={data.get('owner')!r}")
        if not priority_ok:
            print(f"   priority expected={ex['priority']!r} got={data.get('priority')!r}")
        time.sleep(1)

    n = len(examples)
    print(f"\nIntent=task: {is_task}/{n} = {is_task / n:.0%}")
    for name, count in scores.items():
        print(f"{name}: {count}/{n} = {count / n:.0%}")


if __name__ == "__main__":
    run()
