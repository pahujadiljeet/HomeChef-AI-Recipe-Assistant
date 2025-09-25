import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "homechef.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # ✅ Favorites table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id TEXT UNIQUE,
        title TEXT,
        image_path TEXT
    )
    """)

    # ✅ Grocery list table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS grocery_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()
