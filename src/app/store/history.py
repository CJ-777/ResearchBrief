import sqlite3
import json
from typing import List
from src.app.schemas import FinalBrief

DB_PATH = "history.db"


# --- DB setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS briefs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            topic TEXT NOT NULL,
            brief_json TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


# --- Save a brief ---
def save_brief(user_id: str, brief: FinalBrief):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO briefs (user_id, topic, brief_json) VALUES (?, ?, ?)",
        (user_id, brief.topic, brief.json()),
    )
    conn.commit()
    conn.close()


# --- Load briefs for a user ---
def load_user_history(user_id: str, limit: int = 10) -> List[FinalBrief]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT brief_json FROM briefs WHERE user_id = ? ORDER BY id DESC LIMIT ?",
        (user_id, limit),
    )
    rows = cursor.fetchall()
    conn.close()

    briefs = []
    for (brief_json,) in rows:
        briefs.append(FinalBrief.parse_raw(brief_json))
    return briefs
