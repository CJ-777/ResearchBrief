import sqlite3
from typing import List
from src.app.schemas import FinalBrief

DB_PATH = "history.db"


# --- DB setup ---
def init_db():
    """Initialize the SQLite database and create the briefs table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
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


init_db()


# --- Save a brief ---
def save_brief(user_id: str, brief: FinalBrief):
    """Save a FinalBrief object to the database for a specific user."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO briefs (user_id, topic, brief_json) VALUES (?, ?, ?)",
            (user_id, brief.topic, brief.json()),
        )
        conn.commit()


# --- Load briefs for a user ---
def load_user_history(user_id: str, limit: int = 10) -> List[FinalBrief]:
    """Load the most recent FinalBriefs for a user."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT brief_json FROM briefs WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        )
        rows = cursor.fetchall()

    briefs: List[FinalBrief] = [FinalBrief.parse_raw(row[0]) for row in rows]
    return briefs
