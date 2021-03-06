from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from notes.utils import getUserNotes, postUserNote, getUserNote, updateUserNote, deleteUserNote

notes = Blueprint('notes', __name__)

@notes.route('/api/notes', methods=['GET', 'POST'])
@jwt_required
def userNotes():
    claims = get_jwt_claims()
    user_id = claims.get('user_id')
    
    if not user_id:
        return jsonify({'message': 'Missing user_id in Token'}), 400
    
    if request.method == 'GET':
        return getUserNotes(user_id)

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        note_title = content.get("note_title", None)
        note_content = content.get("note_content", None)
        completed = content.get("completed", None)
        if not note_title:
            return jsonify({"message": "Missing note_title"}), 400
        if not note_content:
            return jsonify({"message": "Missing note_content"}), 400
        return postUserNote(note_title, note_content, completed, user_id)

@notes.route('/api/note/<int:note_id>', methods=['GET', 'PUT', 'DELETE']) 
@jwt_required
def userNote(note_id):

    if not note_id:
        return jsonify({"message": "Missing note_id in request"}), 404

    claims = get_jwt_claims()
    user_id = claims.get('user_id')
    
    if not user_id:
        return jsonify({'message': 'Missing user_id in Token'}), 400

    if request.method == 'GET':
        return getUserNote(note_id, user_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        note_title = content['note_title'] if 'note_title' in content.keys() else ''
        note_content = content['note_content'] if 'note_content' in content.keys() else ''
        completed = content['completed'] if 'completed' in content.keys() else False
        return updateUserNote(note_id, note_title, note_content, completed, user_id)

    if request.method == 'DELETE':
        return deleteUserNote(note_id, user_id)
