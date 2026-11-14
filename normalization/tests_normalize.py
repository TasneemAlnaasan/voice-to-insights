
from normalize import normalize_arabic
from normalize import same_name

cases = {
    "أَحْمَد": "احمد",
    "إبراهيم": "ابراهيم",
    "آمال": "امال",
    "مدرســـة": "مدرسة",
    "على": "علي",
    "١٢٣": "123",
    " hello world ": "hello world",
}

for given, expected in cases.items():
    got = normalize_arabic(given)
    print("OK " if got == expected else "FAIL", repr(given), "->", repr(got))

name_cases = [
    ("أحمد", "احمد", True),
    ("Sarah", "sarah", True),
    ("إبراهيم", "ابراهيم", True),
    (None, None, True),
    (None, "سارة", False),
    ("أحمد", "Ahmed", False),
]

for a, b, expected in name_cases:
    got = same_name(a, b)
    print("OK " if got == expected else "FAIL", repr(a), repr(b), "->", got)

