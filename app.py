from flask import Flask, request
from db import get_note, get_db, note_to_dict

app = Flask(__name__)


@app.get("/notes")
def get_notes():
    db = get_db()
    rows = db.execute("SELECT * FROM notes").fetchall()
    return [note_to_dict(r) for r in rows]

@app.post("/notes")
def add_notes():
    data = request.get_json(silent=True)
    if data and "note" in data:
        db = get_db()
        cur = db.execute("INSERT INTO notes (note) VALUES (?)", (data["note"],))
        db.commit()
        new_id = cur.lastrowid
        return {"id": new_id, "note": data["note"], "done": False}, 201
    return {"error": "Invalid data, 'note' key required"}, 400

@app.get("/notes/<int:note_id>")
def get_note_by_id(note_id: int):
    note = get_note(note_id)
    if note is None:
        return {"error": "Note Not Found!"}, 404
    return note

@app.delete("/notes/<int:note_id>")
def delete_note(note_id: int):
    note = get_note(note_id)
    if note is None:
        return {"error": "Note Not Found!"}, 404
    db = get_db()
    db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    return {"status": "Note removed"}, 200
    

@app.put("/notes/<int:note_id>")
def edit_the_note(note_id: int):
    data = request.get_json(silent=True)
    if not data or ("note" not in data and "done" not in data):
        return {"error": "Send 'note' and/or 'done'"}, 400
    if "done" in data and not isinstance(data["done"], bool):
        return {"error": "'done' must be true or false"}, 400
    
    note = get_note(note_id)
    if note is None:
        return {"error": "Note Not Found!"}, 404

    db = get_db()
    if "note" in data:
        db.execute("UPDATE notes SET note = ? WHERE id = ?", (data["note"], note_id))
    if "done" in data:
        db.execute("UPDATE notes SET done = ?  WHERE id = ?", (data["done"], note_id))
    db.commit()
    note = get_note(note_id)
    return note, 200