from flask import jsonify, make_response
from models import Note, User
from __init__ import db

def getUserNotes(user_id):
    notes = Note.query.filter_by(user_id=user_id).all()
    if not notes: 
        return jsonify({"message": "Notes not found"}), 404
    return jsonify(notes=[note.serialize for note in notes])

def postUserNote(note_title, note_content, completed, user_id):
    note = Note(note_title=note_title, note_content=note_content, completed=completed, user_id=user_id)
    db.session.add(note)
    try:
        db.session.commit()
        return jsonify(note=note.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add note to DB"}), 400

def getUserNote(note_id, user_id):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"message": "User not found"}), 404
    note = Note.query.get(note_id)
    if not note: 
        return jsonify({"message": "Note not found"}), 404
    if note.user_id != user.user_id:
        return jsonify({"message": "Unauthorized Access"}), 401
    return jsonify(note=note.serialize)

def updateUserNote(note_id, note_title, note_content, completed, user_id):
    note = Note.query.get(note_id)
    if not note: 
        return jsonify({"message": "Note not found"}), 404
    if note.user_id != user_id:
        return jsonify({"message": "Unauthorized Access"}), 401
    if note_title:
        note.note_title = note_title
    if note_content:
        note.note_content = note_content
    if completed != None:
        note.completed = completed
    db.session.add(note)
    try:
        db.session.commit()
        return jsonify(note=note.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add user to DB"})

def deleteUserNote(note_id, user_id):
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
