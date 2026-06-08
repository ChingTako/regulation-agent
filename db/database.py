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
            source TEXT,
            summary TEXT
        )
    """)

    conn.commit()

    c.execute("PRAGMA table_info(regulations)")
    columns = [row[1] for row in c.fetchall()]
    if "summary" not in columns:
        c.execute("ALTER TABLE regulations ADD COLUMN summary TEXT")
        conn.commit()
    conn.close()


def insert_regulation(title, url, source, summary=None):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO regulations (title, url, source, summary)
            VALUES (?, ?, ?, ?)
        """, (title, url, source, summary or ""))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # URL already exists (unique constraint)
        return False

    except Exception as e:
        print("DB insert failed:", e)
        return False

    finally:
        conn.close()