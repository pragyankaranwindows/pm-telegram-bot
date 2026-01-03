import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Allowed users
cursor.execute("""
CREATE TABLE IF NOT EXISTS allowed_users (
    user_id INTEGER PRIMARY KEY
)
""")

# Admin users
cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    user_id INTEGER PRIMARY KEY
)
""")

conn.commit()

# -------- ALLOWED USERS --------
def add_user(user_id: int):
    cursor.execute("INSERT OR IGNORE INTO allowed_users VALUES (?)", (user_id,))
    conn.commit()

def remove_user(user_id: int):
    cursor.execute("DELETE FROM allowed_users WHERE user_id = ?", (user_id,))
    conn.commit()

def list_users():
    cursor.execute("SELECT user_id FROM allowed_users")
    return [row[0] for row in cursor.fetchall()]

# -------- ADMINS --------
def add_admin(user_id: int):
    cursor.execute("INSERT OR IGNORE INTO admins VALUES (?)", (user_id,))
    conn.commit()

def remove_admin(user_id: int):
    cursor.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
    conn.commit()

def list_admins():
    cursor.execute("SELECT user_id FROM admins")
    return [row[0] for row in cursor.fetchall()]

def is_admin(user_id: int) -> bool:
    cursor.execute("SELECT 1 FROM admins WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None
