"""SQLite persistence layer."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from config import DB_PATH


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                author TEXT NOT NULL,
                url TEXT,
                text TEXT,
                source TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS engagement_suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT NOT NULL,
                suggestion TEXT NOT NULL,
                source TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT NOT NULL,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                source TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS safety_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                detail TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS agent_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mode TEXT NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                outcome TEXT
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            """
        )
        self.conn.commit()

    @staticmethod
    def _now():
        return datetime.now(timezone.utc).isoformat()

    def post_seen(self, post_id):
        row = self.conn.execute("SELECT 1 FROM posts WHERE id=?", (post_id,)).fetchone()
        return row is not None

    def upsert_post(self, post_id, author, url, text, source):
        self.conn.execute(
            """
            INSERT OR REPLACE INTO posts(id, author, url, text, source, created_at)
            VALUES(?,?,?,?,?,?)
            """,
            (post_id, author, url, text, source, self._now()),
        )
        self.conn.commit()

    def save_suggestion(self, post_id, suggestion, source):
        self.conn.execute(
            """
            INSERT INTO engagement_suggestions(post_id, suggestion, source, created_at)
            VALUES(?,?,?,?)
            """,
            (post_id, suggestion, source, self._now()),
        )
        self.conn.commit()

    def record_action(self, post_id, action, status, source):
        self.conn.execute(
            """
            INSERT INTO actions(post_id, action, status, source, created_at)
            VALUES(?,?,?,?,?)
            """,
            (post_id, action, status, source, self._now()),
        )
        self.conn.commit()

    def record_safety_event(self, event_type, detail):
        self.conn.execute(
            "INSERT INTO safety_events(event_type, detail, created_at) VALUES(?,?,?)",
            (event_type, detail, self._now()),
        )
        self.conn.commit()

    def open_session(self, mode):
        cur = self.conn.execute(
            "INSERT INTO agent_sessions(mode, started_at) VALUES(?,?)",
            (mode, self._now()),
        )
        self.conn.commit()
        return cur.lastrowid

    def close_session(self, outcome):
        row = self.conn.execute(
            "SELECT id FROM agent_sessions WHERE ended_at IS NULL ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if row:
            self.conn.execute(
                "UPDATE agent_sessions SET ended_at=?, outcome=? WHERE id=?",
                (self._now(), outcome, row["id"]),
            )
            self.conn.commit()

    def recover(self):
        self.conn.execute(
            "UPDATE actions SET status='CANCELLED_ON_RESTART' "
            "WHERE status='PENDING_APPROVAL'"
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
