# 🎙️ Voice-to-Insight Agent

Arabic / English voice or text note → classify → act.

**Live demo:** https://voice-to-insight.streamlit.app/

> The demo's task list is shared between all visitors and resets when the app restarts. Please don't enter personal information.

## What it does

Record a voice note or upload any audio/video file, or just type a note. The audio is transcribed with Whisper, then the text is classified into one of four intents and acted on:

| Intent | What happens |
|---|---|
| `task` | Extracts title, owner, due date and priority, and adds it to the task list |
| `content` | Writes a caption/post for a platform and tone |
| `summary` | Summarizes only what the speaker said |
| `question` | Answers from my notes (RAG) and shows the top source section |

## Pipeline

```
voice / text → stt.transcribe → understand.understand → {intent, data} → actions.dispatch → UI
```

A small input filter sits in front of the classifier to block prompt-injection attempts.

## Results

Every number below comes from a script in `evals/` that writes its output to `evals/result_*.txt`.

| Eval | Cases | Result |
|---|---|---|
| Intent classification | 46 | 46/46 (100%) |
| Task fields: owner | 36 | 35/36 (97%) |
| Task fields: priority | 36 | 32/36 (89%) |
| Task fields: due date | 36 | 34/36 (94%) |
| Prompt injection | 7 (5 attacks + 2 legitimate inputs) | 2 of 5 attacks succeeded, 3 blocked by the filter, 2/2 legitimate inputs passed |
| RAG retrieval | 19 | Hit@1 14/19 (74%), Hit@3 18/19 (95%) |

**Cost:** the 46-case intent eval used 59,603 tokens (about 1,300 per request).

> These eval sets are small and I used them while tuning prompts, so treat them as development numbers, not benchmarks or security guarantees.

## What I found along the way

**1. The summarizer invented content.** Early summaries padded the output: they added "No other topics mentioned" (not in the note), repeated points, and for a voice note about the "Transformers" lesson it produced an explanation about Fourier transforms, because it read "transformers" as a math term. I added a rule to summarize only what the speaker said. After the fix, a one-line request gets a one-line summary with no extra explanation. I checked this by hand on a few sentences. The evals don't measure invention, so it can still happen.

**2. Speech-to-text errors flow into classification.** Whisper wrote "لكرني" instead of "ذكرني" in two recordings, and the classifier then labelled the note `summary` instead of `task`. The same sentence typed with "ذكرني" was classified as `task`, so the classifier is fine and the error comes from transcription. Both recordings used a text-to-speech voice, not a human speaker, so I don't know yet how often this happens with real speech.

**3. "Not urgent" phrases become `medium` priority.** All 4 priority misses have the same shape: the note says something like "whenever I get a chance" or "no rush", the expected priority is `low`, and the model returns `medium`. In 2 of those 4 the due date was also wrong.

**4. Names can come back in a different script.** In one case the expected owner was an Arabic name and the model returned it in Latin letters. The meaning is right, but the exact-match check fails.

## Known limits

- Eval sets are small and were used during tuning (see above).
- The injection filter is not a security guarantee: 2 of 5 attacks still got through.
- Retrieval ranks the right section first in 74% of eval cases (and within the top 3 in 95%), so the single source shown under an answer is not always the section that held the answer.
- The prompt asks for an answer in the question's language, but an English question got an Arabic answer (the notes are in Arabic). The content was right.
- Outputs can vary between runs: one Arabic sentence got `low` priority in the live app but `medium` in an eval run.
- Groq rate limits can stop an eval run halfway, so I run the evals one at a time and re-run if a run is cut off.

## Next steps

- Fix soft-timing phrases ("whenever I can") so they map to `low` priority, and test the fix on new sentences the prompt hasn't seen.
- Test speech-to-text on real human recordings, then decide whether a transcription hint or a correction step helps.
- Make the answer follow the question's language more reliably.
- Keep tasks per visitor (session state) instead of one shared list.

## Run locally

```bash
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
streamlit run streamlit_app.py
```

On Streamlit Community Cloud, put `GROQ_API_KEY` in the app's Secrets instead of the repo.

Run an eval (one at a time):

```bash
python evals/run_fields.py | tee evals/result_fields.txt
python evals/run_injection.py | tee evals/result_injection.txt
```

## Repo layout

```
streamlit_app.py   UI: voice, text, task list
stt.py             speech-to-text
understand.py      intent classification + extraction
actions.py         what each intent does
db.py              SQLite task storage
guardrails.py      injection scan (also applied to retrieved notes)
rag/               retrieval + answer
evals/             eval sets, scripts and saved results
```

## Credit

Started from the Day 3 voice-to-insights project in Lara Wehbe's Shift to AI Engineering series. This repo documents my own evaluations and improvements.

