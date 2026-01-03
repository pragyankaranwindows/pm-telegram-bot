import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS allowed_users (
    user_id INTEGER PRIMARY KEY
)
""")

conn.commit()

def add_user(user_id: int):
    cursor.execute(
        "INSERT OR IGNORE INTO allowed_users (user_id) VALUES (?)",
        (user_id,)
    )
    conn.commit()

def remove_user(user_id: int):
    cursor.execute(
        "DELETE FROM allowed_users WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()

def is_allowed(user_id: int) -> bool:
    cursor.execute(
        "SELECT 1 FROM allowed_users WHERE user_id = ?",
        (user_id,)
    )
    return cursor.fetchone() is not None

def list_users():
    cursor.execute("SELECT user_id FROM allowed_users")
    return [row[0] for row in cursor.fetchall()]
