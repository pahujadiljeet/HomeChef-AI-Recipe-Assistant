import sqlite3

def create_tables():
    conn = sqlite3.connect("homechef.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT NOT NULL,
        cook_time TEXT,
        difficulty TEXT,
        image_path TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pantry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grocery_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name TEXT NOT NULL,
        status TEXT DEFAULT "needed"
    )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database aur tables create ho gaye.")

if __name__ == "__main__":
    create_tables()
