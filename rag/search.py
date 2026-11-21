
import numpy as np
from fastembed import TextEmbedding

from rag.chunking import load_chunks

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

_model = None 
_index = None


def _get_model():
    global _model
    if _model is None:
        _model = TextEmbedding(model_name=MODEL_NAME)
    return _model


def _embed(texts):
    vectors = np.array(list(_get_model().embed(texts)))
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


def _get_index():
    global _index
    if _index is None:
        chunks = load_chunks()
        _index = (chunks, _embed([c["text"] for c in chunks]))
    return _index


def search(question, k=3):
    chunks, vectors = _get_index()
    q = _embed([question])[0]
    scores = vectors @ q 
    top = np.argsort(scores)[::-1][:k] 
    return [{**chunks[i], "score": float(scores[i])} for i in top]
