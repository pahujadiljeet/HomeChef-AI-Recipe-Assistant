import sqlite3
from backend.gpt_api import ask_ai

DB_PATH = "homechef.db"

def find_recipes_by_ingredients(user_ingredients: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # User input ko lowercase list banado
    user_ingredients_list = [i.strip().lower() for i in user_ingredients.split(",")]

    # DB se sari recipes fetch karo
    cursor.execute("SELECT id, title, ingredients FROM recipes")
    all_recipes = cursor.fetchall()

    matching_recipes = []
    for recipe_id, title, ingredients in all_recipes:
        # Agar sare ingredients match karte hain
        if all(item in ingredients.lower() for item in user_ingredients_list):
            matching_recipes.append((recipe_id, title))

    conn.close()

    if matching_recipes:
        return {"type": "db", "data": matching_recipes}
    else:
        # Agar DB me match nahi mila → AI ko call karo
        ai_prompt = f"Suggest a recipe idea using only these ingredients: {', '.join(user_ingredients_list)}"
        ai_response = ask_ai(ai_prompt)
        return {"type": "ai", "data": ai_response}
