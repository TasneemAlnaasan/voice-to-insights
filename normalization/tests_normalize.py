
from normalize import normalize_arabic

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

