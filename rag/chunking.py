
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "documents"


def _add(chunks, h1, h2, body):
 
    content = "\n".join(body).strip()
    if h2 and content:
        title = f"{h1} / {h2}"
       
        chunks.append({"id": len(chunks), "title": title, "text": f"{title}\n{content}"})


def load_chunks(path=None):
    path = Path(path) if path else DOCS_DIR / "agents_notes.md"
    text = path.read_text(encoding="utf-8")

    chunks = []
    h1, h2, body = "", None, []

    for line in text.splitlines():
        if line.startswith("# "):
           
            _add(chunks, h1, h2, body)
            h1, h2, body = line[2:].strip(), None, []
        elif line.startswith("## "):
            
            _add(chunks, h1, h2, body)
            h2, body = line[3:].strip(), []
        else:
            body.append(line)

    _add(chunks, h1, h2, body)
    return chunks
