from flask import Flask, request

app = Flask(__name__)
notes = []
next_id = 1

def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    return None

@app.get("/notes")
def get_notes():
    return notes

@app.post("/notes")
def add_notes():
    global next_id
    data = request.get_json(silent=True)

    if data and "note" in data:
        new_note = {"id": next_id, "note": data["note"], "done": False}
        notes.append(new_note)
        next_id += 1
        return new_note, 201
    return {"error": "Invalid data, 'note' key required" }, 400

@app.get("/notes/<int:note_id>")
def get_note_by_id(note_id: int):
    note = get_note(note_id)
    if not note:
        return {"error": "Note Not Found!"}, 404
    return note

@app.delete("/notes/<int:note_id>")
def delete_note(note_id: int):
    note = get_note(note_id)
    if note is None:
        return {"error": "Note Not Found!"}, 404
    notes.remove(note)
    return {"status": "Note removed"}, 200
    

@app.put("/notes/<int:note_id>")
def edit_the_note(note_id: int):
    data = request.get_json(silent=True)
    if not data and data[""]:
        return {"error": "Invalid data, 'note' key required"}, 400
    if "done" in data and not isinstance(data["done"], bool):
        return {"error": "'done' must be true or false"}, 400
    note = get_note(note_id)

    if note is None:
        return {"error": "Note Not Found!"}, 404
    if "note" in data:
        note["note"] = data["note"]
    if "done" in data:
        note["done"] = data["done"]
    return note, 200