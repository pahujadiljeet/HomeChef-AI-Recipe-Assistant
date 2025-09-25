import tkinter as tk
from tkinter import ttk, messagebox
import openai

# ✅ Apni API key yahan dalni hai
openai.api_key = "YOUR_API_KEY_HERE"

class SuggestionsWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Smart Recipe Suggestions")
        self.geometry("600x400")

        # ✅ Ingredients input
        tk.Label(self, text="Enter available ingredients:", font=("Arial", 12)).pack(pady=5)
        self.ingredients_entry = tk.Entry(self, width=50)
        self.ingredients_entry.pack(pady=5)

        # ✅ Button
        ttk.Button(self, text="Get Recipe Suggestions", command=self.get_suggestions).pack(pady=10)

        # ✅ Output area
        self.result_box = tk.Text(self, wrap="word", height=15, width=70)
        self.result_box.pack(pady=10)

        # ✅ Back Button
        ttk.Button(self, text="Back to Home", command=self.go_back).pack(pady=10)

    def get_suggestions(self):
        ingredients = self.ingredients_entry.get().strip()
        if not ingredients:
            messagebox.showwarning("Warning", "Please enter at least one ingredient.")
            return

        try:
            # ✅ GPT API call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # ya gpt-4 agar available ho
                messages=[
                    {"role": "system", "content": "You are a helpful chef assistant."},
                    {"role": "user", "content": f"Suggest a recipe using these ingredients: {ingredients}. "
                                                f"If no exact recipe exists, suggest creative alternatives and substitutions."}
                ],
                max_tokens=300
            )

            suggestion = response["choices"][0]["message"]["content"]

            # ✅ Show in text box
            self.result_box.delete(1.0, tk.END)
            self.result_box.insert(tk.END, suggestion)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch suggestions: {e}")

    def go_back(self):
        self.destroy()
