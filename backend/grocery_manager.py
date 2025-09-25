from .database import get_connection

def add_item(item_name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO grocery_list (item) VALUES (?)", (item_name,))
        conn.commit()
    except Exception:
        pass  # agar item already exist hai to ignore kar do
    conn.close()

def get_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM grocery_list")
    rows = cur.fetchall()
    conn.close()
    return rows

def remove_item(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM grocery_list WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
