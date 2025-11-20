import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "data.db"

def init():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT
        )
    """)
    # You can change/add FAQ entries
    faqs = [
        ("how to make maggi", "To make Maggi: boil water, add noodles and masala, cook for 2 minutes."),
        ("what is your refund policy", "You can request a refund within 14 days; contact support."),
        ("opening hours", "We are open 9 AM to 6 PM Monday to Friday."),
    ]
    cur.executemany("INSERT INTO faqs (question, answer) VALUES (?, ?)", faqs)
    conn.commit()
    conn.close()
    print("DB initialized:", DB)

if __name__ == "__main__":
    init()
