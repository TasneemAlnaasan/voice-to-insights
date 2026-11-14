import re

DIACRITICS = re.compile(r"[\u064B-\u0652\u0670]")

TATWEEL = "\u0640"

TABLE = str.maketrans({
    "أ": "ا", "إ": "ا", "آ": "ا", 
    "ى": "ي",
    "٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4",
    "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9", 
})


def normalize_arabic(text: str) -> str:
    text = DIACRITICS.sub("", text) 
    text = text.replace(TATWEEL, "")
    text = text.translate(TABLE) 
    return " ".join(text.split())
