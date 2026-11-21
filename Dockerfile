
FROM python:3.14.2

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV EMBED_CACHE=$HOME/app/.fastembed
RUN python -c "import os; from fastembed import TextEmbedding; TextEmbedding(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', cache_dir=os.environ['EMBED_CACHE'])"

COPY --chown=user . .

EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]