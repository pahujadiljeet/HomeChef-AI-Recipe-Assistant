import sqlite3
import os

# Database path
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'homechef.db'))

def insert_sample():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Sample recipes (ingredients in lowercase for better matching)
    samples = [
        (
            "Pasta with Tomato Sauce",
            "pasta, tomato, garlic, salt, olive oil".lower(),
            "1. Boil pasta.\n2. Sauté garlic, add tomatoes to make sauce.\n3. Mix pasta with sauce and serve.",
            "20 minutes",
            "Easy",
            "assets/pasta.jpg"
        ),
        (
            "Simple Pancakes",
            "flour, milk, egg, sugar, baking powder, salt, oil".lower(),
            "1. Mix dry ingredients.\n2. Add milk and egg; whisk.\n3. Cook batter on skillet until golden brown.",
            "15 minutes",
            "Easy",
            "assets/pancakes.jpg"
        )
    ]

    # Insert recipes
    for s in samples:
        cur.execute(
            "INSERT INTO recipes (title, ingredients, instructions, cook_time, difficulty, image_path) VALUES (?,?,?,?,?,?)",
            s
        )

    conn.commit()
    conn.close()
    print("✅ Sample recipes inserted successfully.")

if __name__ == "__main__":
    insert_sample()
