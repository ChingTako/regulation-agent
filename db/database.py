import sqlite3

DB = "regulations.db"

def init_db():

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS regulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            source TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_regulation(title, url, source):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO regulations (title, url, source)
            VALUES (?, ?, ?)
        """, (title, url, source))

        conn.commit()
        return True

    except:
        return False

    finally:
        conn.close()