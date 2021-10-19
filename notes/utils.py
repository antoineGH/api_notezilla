from flask import jsonify, make_response
from models import Note, User
from __init__ import db

def getUserTodos(user_id):
    notes = Note.query.filter_by(user_id=user_id).all()
    if not notes: 
        return jsonify({"message": "Todos not found"}), 404
    return jsonify(notes=[note.serialize for note in notes])

def postUserTodo(note_description, completed, user_id):
    note = Note(note_description=note_description, completed=completed, user_id=user_id)
    db.session.add(note)
    try:
        db.session.commit()
        return jsonify(note=note.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add note to DB"}), 400

def getUserTodo(note_id, user_id):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"message": "User not found"}), 404
    note = Note.query.get(note_id)
    if not note: 
        return jsonify({"message": "Note not found"}), 404
    if note.user_id != user.user_id:
        return jsonify({"message": "Unauthorized Access"}), 401
    return jsonify(note=note.serialize)

def updateUserTodo(note_id, note_description, completed, user_id):
    note = Note.query.get(note_id)
    if not note: 
        return jsonify({"message": "Note not found"}), 404
    if note.user_id != user_id:
        return jsonify({"message": "Unauthorized Access"}), 401
    if note_description:
        note.note_description = note_description
    if completed != None:
        note.completed = completed
    db.session.add(note)
    try:
        db.session.commit()
        return jsonify(note=note.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add user to DB"})

def deleteUserTodo(note_id, user_id):
    note = Note.query.get(note_id)
    if not note: 
        return jsonify({"message": "Note not found"}), 404
    if note.user_id != user_id:
        return jsonify({"message": "Unauthorized Access"}), 401
    db.session.delete(note)
    try:
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)