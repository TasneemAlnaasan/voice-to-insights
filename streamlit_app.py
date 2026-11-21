import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

try:
    if "GROQ_API_KEY" in st.secrets and not os.getenv("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

import actions
import db
import stt
import understand

db.init_db()

SAMPLES = [
    "Remind Sarah to send the Q3 report by next Friday, it's high priority.",
    "اكتبلي بوست عن الإنجازات تبعنا هالشهر للينكد إن، بطريقة احترافية.",
    "Summarize this: we met the client, they liked the demo, but want pricing options.",
    "مين مسؤول عن الـ README؟",
]


def show_action(a):
    kind = a.get("type")
    if kind == "task_added":
        st.success("Task added: " + a["task"]["title"])
    elif kind == "caption_generated":
        st.markdown(f"**Caption for {a.get('platform')}** ({a.get('tone') or ''})")
        st.info(a.get("caption", ""))  
    elif kind == "summary_shown":
        st.markdown(a.get("summary_text", ""))
        for p in a.get("key_points", []):
            st.markdown("- " + p)
    elif kind == "answer_generated":
        if a.get("error"):
            st.warning(a["error"])
        st.markdown(a.get("answer", ""))
        if a.get("sources"):
            st.caption("Sources: " + " | ".join(a["sources"]))
    else:
        st.write(a)


def transcribe_bytes(data, filename):
    suffix = os.path.splitext(filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(data)
        path = f.name
    try:
        return stt.transcribe(path)
    finally:
        os.remove(path)


def run_pipeline(text):
    with st.spinner("Understanding…"):
        result = understand.understand(text)
    if result["intent"] == "error":
        st.error(result["error"])
        return
    st.subheader("Classification: " + result["intent"])
    st.json(result["data"])
    show_action(actions.dispatch(result["intent"], result["data"]))


st.set_page_config(page_title="Voice-to-Insight", page_icon="🎙️")
st.title("🎙️ Voice-to-Insight Agent")
st.caption("Arabic / English note → classify → act")

st.subheader("1 · Voice")
recorded = st.audio_input("Record a voice note")
uploaded = st.file_uploader(
    "…or upload a voice note", type=["wav", "mp3", "m4a", "mp4", "webm", "ogg"]
)
if st.button("Transcribe + run voice note"):
    audio = recorded if recorded is not None else uploaded
    if audio is None:
        st.warning("Record or upload audio first.")
    else:
        try:
            with st.spinner("Transcribing…"):
                tr = transcribe_bytes(audio.getvalue(), getattr(audio, "name", None) or "audio.wav")
        except Exception as exc:
            st.error(f"Transcription failed: {exc}")
        else:
            st.session_state["note"] = tr["transcript"]
            st.session_state["auto_run"] = True


st.subheader("2 · Text")
cols = st.columns(len(SAMPLES))
for i, (col, sample) in enumerate(zip(cols, SAMPLES)):
    if col.button(f"Sample {i + 1}", help=sample, key=f"sample{i}"):
        st.session_state["note"] = sample

text = st.text_area("Type or paste a note", key="note", height=120)
clicked = st.button("Run → understand", type="primary")
auto = st.session_state.pop("auto_run", False)

if clicked or auto:
    if not text.strip():
        st.warning("Type or pick a sample first.")
    else:
        run_pipeline(text)

st.divider()
st.subheader("Running tasks")
tasks = db.list_tasks()
if not tasks:
    st.caption("No tasks yet.")
for t in tasks:
    st.markdown(f"**{t['title']}**  \n{t['priority']} · {t.get('owner') or ''} · {t.get('due_date') or ''}")
