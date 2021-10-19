from flask import jsonify, make_response
from models import User, Note
from __init__ import bcrypt, db
from flask_jwt_extended import get_jwt_identity

def isAdmin():
    current_user = get_jwt_identity()
    return current_user == 'antoine.ratat@gmail.com'

def getUsers():
    users = User.query.all()
    return jsonify(users=[user.serialize for user in users])

def postUser(email, password, first_name, last_name):
    userExisting = User.query.filter_by(email=email).first()
    if userExisting:
        return jsonify({'message': 'User already exists'}), 400
    hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=hashedPassword, first_name=first_name, last_name=last_name)
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(user=user.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add user to DB"}), 400

def getUser(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User doesn\'t exist"}), 404
    return jsonify(user=user.serialize)

def updateUser(user_id, email, password, first_name, last_name):
    user = User.query.get(user_id)
    print(user)
    if not user:
        return jsonify({"message": 'User doesn\'t exist'}), 404
    if email:
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            if int(existing_email.user_id != int(user_id)):
                return jsonify({"message": "Email already existing"}), 404
        user.email = email
    if password:
        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = hashedPassword
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(user=user.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add user to DB"})

def deleteUser(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User doesn't exist"}), 404
    db.session.delete(user)
    try:
        db.session.commit()
        return make_response(jsonify({"message": 'Removed user with ID: {}'.format(user_id)}))
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't delete user to DB"}), 400

def getNotes():
    notes = Note.query.all()
    return jsonify(notes=[note.serialize for note in notes])

def postNote(note_title, note_description, completed, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'No user associated'}), 400
    note = Note(note_title=note_title, note_description=note_description, completed=completed, user_id=user_id)
    db.session.add(note)
    try:
        db.session.commit()
        return jsonify(note=note.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add note to DB"}), 400

def getNote(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"message": "Note doesn\'t exist"}), 404
    return jsonify(note=note.serialize)

def updateNote(note_id, note_title, note_description, completed, user_id):
    user = User.query.get(user_id)
    note = Note.query.get(note_id)
    if not user:
        return jsonify({'message': 'No user associated'}), 400
    if not note:
        return jsonify({'message': 'No note associated'}), 400
    if note_title:
        note.note_title = note_title
    if note_description:
        note.note_description = note_description
    if completed != None:
        note.completed = completed
    if user_id:
        note.user_id = user_id
    db.session.add(note)
    try:
        db.session.commit()
        return jsonify(note=note.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add user to DB"})

def deleteNote(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"message": "Note doesn't exist"}), 404
    db.session.delete(note)
    try:
        db.session.commit()
        return make_response(jsonify({"message": 'Removed note with ID: {}'.format(note_id)}))
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't delete note to DB"}), 400

def getNotesUser(user_id):
    notes = Note.query.filter_by(user_id=user_id).all()
    return jsonify(notes=[note.serialize for note in notes])
