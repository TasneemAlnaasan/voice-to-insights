import re

from normalization.normalize import normalize_arabic

STRUCTURAL_PATTERNS = [
    r"</?\s*transcript\s*>", 
    r"</?\s*instructions?\s*>", 
    r"[\"']kind[\"']\s*:", 
    r"#{3,}", 
    r"\bsystem\s*:", 
]

WORDING_PATTERNS = [
    r"\b(ignore|disregard|forget)\b.{0,25}\b(instructions?|rules|prompt|guidelines)\b",
    r"\bnew (system )?instructions?\b",
    r"\b(reply|respond|answer|output) only (with|in|as)\b",
    r"\bclassify (this|it|the above|everything) as\b",
    r"\bdebug mode\b",
    r"\bfrom now on\b.{0,30}\byou\b",
    r"\bتجاهلي?\b.{0,20}(التعليمات|الاوامر|القواعد)",
    r"\bانسي?\b.{0,25}(التعليمات|الاوامر|القواعد|كل (اللي|ما) (قبل|فوق|سبق))",
    r"\bرد فقط\b",
    r"تعليمات نظام",
]

STRUCTURAL = [re.compile(p) for p in STRUCTURAL_PATTERNS]
WORDING = [re.compile(p) for p in WORDING_PATTERNS]


def scan(text: str) -> str:
    clean = normalize_arabic(text).casefold()

    if any(p.search(clean) for p in STRUCTURAL):
        return "block"

    if any(p.search(clean) for p in WORDING):
        return "warn"

    return "ok"


def looks_like_injection(text: str) -> bool:
    return scan(text) != "ok"

