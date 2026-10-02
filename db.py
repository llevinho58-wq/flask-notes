import sqlite3

def get_db():
    db = sqlite3.connect("notes.db")
    db.row_factory = sqlite3.Row
    db.execute(
    "CREATE TABLE IF NOT EXISTS notes ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "note TEXT NOT NULL, "
    "done INTEGER DEFAULT 0)"
    )
    return db

def note_to_dict(row):
    note = dict(row)
    note["done"] = bool(note["done"])
    return note

def get_note(note_id: int):
    db = get_db()
    row = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        return None
    return note_to_dict(row)