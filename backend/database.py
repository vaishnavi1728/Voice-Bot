import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def get_faq_answer(user_text: str) -> str:
    """
    Simple fuzzy-like FAQ lookup: returns matching FAQ answer if found.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT question, answer FROM faqs")
        rows = cur.fetchall()
        conn.close()

        t = user_text.lower()
        for q, a in rows:
            if q.lower() in t or any(word in t for word in q.lower().split()):
                return a
        return None
    except Exception as e:
        print("DB error:", e)
        return None
