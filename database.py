import sqlite3

def init_db():
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        file_id TEXT,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_photo(username, file_id):
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO photos (username, file_id) VALUES (?, ?)",
        (username, file_id)
    )

    conn.commit()
    conn.close()


def get_all_photos():
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, file_id
    FROM photos
    ORDER BY id DESC
    """)

    photos = cursor.fetchall()

    conn.close()

    return photos