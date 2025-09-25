import sqlite3
import os

DB_NAME = "homechef.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Recipes table (updated schema)
    c.execute('''CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    ingredients TEXT,
                    instructions TEXT,
                    image TEXT,
                    time TEXT,
                    difficulty TEXT
                )''')

    # Favorites table
    c.execute('''CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe_id INTEGER,
                    FOREIGN KEY(recipe_id) REFERENCES recipes(id)
                )''')

    # Grocery list table
    c.execute('''CREATE TABLE IF NOT EXISTS grocery_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item TEXT UNIQUE
                )''')

    conn.commit()
    conn.close()
    insert_sample_recipes()

def add_favorite(recipe_id):
    """Add recipe_id to favorites (INSERT OR IGNORE to avoid duplicates)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # ensure favorites table exists (safe)
    c.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER UNIQUE
        )
    """)
    c.execute("INSERT OR IGNORE INTO favorites (recipe_id) VALUES (?)", (recipe_id,))
    conn.commit()
    conn.close()
    return True

def get_favorites():
    """
    Return list of favorite recipes as list of dicts:
    [{'id':..., 'title':..., 'ingredients': [...], 'instructions':..., 'image':..., 'time':..., 'difficulty':...}, ...]
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # join favorites to recipes to get full details
    c.execute("""
        SELECT r.id, r.name, r.ingredients, r.instructions, r.image, r.time, r.difficulty
        FROM recipes r
        JOIN favorites f ON r.id = f.recipe_id
        ORDER BY f.id DESC
    """)
    rows = c.fetchall()
    conn.close()

    favorites = []
    for r in rows:
        favorites.append({
            'id': r[0],
            'title': r[1],
            'ingredients': [i.strip() for i in r[2].split(',')] if r[2] else [],
            'instructions': r[3] or "",
            'image': r[4] or "",
            'time': r[5] or "",
            'difficulty': r[6] or ""
        })
    return favorites

def remove_favorite(recipe_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE recipe_id = ?", (recipe_id,))
    conn.commit()
    conn.close()
    return True

# ===============================
# Grocery list helper functions
# ===============================

def add_grocery_item(item):
    """Add item to grocery_list (unique constraint handle)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO grocery_list (item) VALUES (?)", (item.strip(),))
    conn.commit()
    conn.close()

def remove_grocery_item(item):
    """Remove item from grocery_list."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM grocery_list WHERE item=?", (item.strip(),))
    conn.commit()
    conn.close()

def get_grocery_items():
    """Return all grocery list items as a Python list of strings."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT item FROM grocery_list ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]



def insert_sample_recipes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM recipes")
    count = c.fetchone()[0]

    if count == 0:
        sample_data = [
            ("Pasta", "Pasta, Tomato Sauce, Cheese",
             "1. Boil pasta\n2. Add sauce\n3. Sprinkle cheese",
             "pasta.png", "20 mins", "Easy"),

            ("Omelette", "Eggs, Salt, Pepper, Oil",
             "1. Beat eggs\n2. Fry with oil\n3. Add salt & pepper",
             "omelette.png", "10 mins", "Easy"),

            ("Grilled Sandwich", "Bread, Cheese, Veggies",
             "1. Stuff bread with cheese & veggies\n2. Grill till golden brown",
             "sandwich.png", "15 mins", "Medium"),
        ]
        c.executemany(
            "INSERT INTO recipes (name, ingredients, instructions, image, time, difficulty) VALUES (?, ?, ?, ?, ?, ?)",
            sample_data
        )
        conn.commit()

    conn.close()


def get_all_recipes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, ingredients, instructions, image, time, difficulty FROM recipes")
    rows = c.fetchall()
    conn.close()
    return rows


def get_all_recipes_dict():
    """Return recipes as list of dicts with extra meta info"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, ingredients, instructions, image, time, difficulty FROM recipes")
    rows = c.fetchall()
    conn.close()
    recipes = []
    for r in rows:
        recipes.append({
            'id': r[0],
            'title': r[1],
            'ingredients': [ing.strip() for ing in r[2].split(',')] if r[2] else [],
            'instructions': r[3],
            'image': r[4],
            'time': r[5],
            'difficulty': r[6]
        })
    return recipes


def add_recipe(name, ingredients, instructions, image=None, time=None, difficulty=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO recipes (name, ingredients, instructions, image, time, difficulty) VALUES (?, ?, ?, ?, ?, ?)",
              (name, ingredients, instructions, image, time, difficulty))
    conn.commit()
    conn.close()


def get_recipe_by_id(recipe_id):
    """Fetch a single recipe by its ID"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, ingredients, instructions, image, time, difficulty FROM recipes WHERE id=?", (recipe_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'id': row[0],
            'title': row[1],
            'ingredients': [i.strip() for i in row[2].split(",")] if row[2] else [],
            'instructions': row[3],
            'image': row[4],
            'time': row[5],
            'difficulty': row[6]
        }
    return None


# ✅ Favorites and Grocery functions remain unchanged...

# Ensure DB is ready
init_db()
