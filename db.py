import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "tasks.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn


def init_db():
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                owner TEXT,
                due_date TEXT,
                priority TEXT,
                created_at TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()

def add_task(task: dict) -> int:
    conn = _connect()
    try:
        cur = conn.execute(
            "INSERT INTO tasks (title, owner, due_date, priority, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                task["title"],
                task.get("owner"),
                task.get("due_date"),
                task.get("priority"),
                task.get("created_at"),
            ),
        )
        conn.commit()
        return cur.lastrowid 
    finally:
        conn.close()

def list_tasks() -> list[dict]:
    conn = _connect()
    try:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
