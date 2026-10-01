import sqlite3

db = sqlite3.connect("notes.db")
db.row_factory = sqlite3.Row

db.execute(
    "CREATE TABLE IF NOT EXISTS notes ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "note TEXT NOT NULL, "
    "done INTEGER DEFAULT 0)"
)
db.execute("INSERT INTO notes (note) VALUES (?)", ("First note",))
db.execute("INSERT INTO notes (note) VALUES (?)", ("Second note",))
db.commit()

for row in db.execute("SELECT * FROM notes").fetchall():
    print(row["id"], row["note"], row["done"])