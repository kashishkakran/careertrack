import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "careertrack.db"

#connect to sqlite
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    return conn

# create tables
def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied',
                date_applied TEXT,
                job_url TEXT,
                notes TEXT,
                next_action TEXT,
                deadline TEXT,
                recruiter_name TEXT,
                recruiter_email TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

def create_demo_user():
    conn = get_connection()

    try:
        conn.execute(
            "INSERT OR IGNORE INTO users (email) VALUES (?)",
            ("demo@careertrack.local",)
        )

        conn.commit()

        cursor = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            ("demo@careertrack.local",)
        )

        return cursor.fetchone()[0]

    finally:
        conn.close()

def add_application(user_id, company, role, status, date_applied):
    conn = get_connection()

    try:
        conn.execute("""
            INSERT INTO applications
            (user_id, company, role, status, date_applied)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, company, role, status, date_applied))

        conn.commit()

        print("Application saved successfully!")

    finally:
        conn.close()

if __name__ == "__main__":
    init_db()

    user_id = create_demo_user()

    print("Database initialised successfully!")
    print(f"Demo user ID: {user_id}")

    add_application(
        user_id,
        "MongoDB",
        "Software Engineering intern",
        "Applied",
        "2026-10-22"
    )

def get_applications(user_id):
    conn = get_connection()

    try:
        conn.row_factory = sqlite3.Row

        cursor = conn.execute("""
            SELECT id, company, role, status, date_applied
            FROM applications
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        conn.close()

