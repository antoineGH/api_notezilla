from flask import jsonify
from models import User, Scratch
from __init__ import db

def getUserScratch(user_id):
    scratchs = Scratch.query.filter_by(user_id=user_id).all()
    if not scratchs: 
        return jsonify({"message": "Scratch not found"}), 404
    return jsonify(scratch=[scratch.serialize for scratch in scratchs])

def postUserScratch(scratch_title, scratch_content, completed, user_id):
    existing_scratch = Scratch.query.filter_by(user_id=user_id).first()
    if existing_scratch:
        return updateUserScratch(existing_scratch.scratch_id, scratch_title, scratch_content, completed, user_id)
    scratch = Scratch(scratch_title=scratch_title, scratch_content=scratch_content, completed=completed, user_id=user_id)
    db.session.add(scratch)
    try:
        db.session.commit()
        return jsonify(scratch=scratch.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add scratch to DB"}), 400

def updateUserScratch(scratch_id, scratch_title, scratch_content, completed, user_id):
    scratch = Scratch.query.get(scratch_id)
    if not scratch: 
        return jsonify({"message": "Scratch not found"}), 404
    if scratch.user_id != user_id:
        return jsonify({"message": "Unauthorized Access"}), 401
    if scratch_title:
        scratch.scratch_title = scratch_title
    if scratch_content:
        scratch.scratch_content = scratch_content
    if completed != None:
        scratch.completed = completed
    db.session.add(scratch)
    try:
        db.session.commit()
        return jsonify(scratch=scratch.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add user to DB"})

def deleteUserScratch(user_id):
    scratch = Scratch.query.filter_by(user_id=user_id).first()
    if not scratch: 
        return jsonify({"message": "Scratch not found"}), 404
    if scratch.user_id != user_id:
        return jsonify({"message": "Unauthorized Access"}), 401
    return updateUserScratch(scratch.scratch_id, 'lol', 'lol', False, scratch.user_id)