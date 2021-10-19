from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from notes.utils import getUserNotes, postUserTodo, getUserTodo, updateUserTodo, deleteUserTodo

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
        note_description = content.get("note_description", None)
        completed = content.get("completed", None)
        if not note_description:
            return jsonify({"message": "Missing note_description"}), 400
        return postUserTodo(note_description, completed, user_id)

@notes.route('/api/note/<int:note_id>', methods=['GET', 'PUT', 'DELETE']) 
@jwt_required
def userTodo(note_id):

    if not note_id:
        return jsonify({"message": "Missing note_id in request"}), 404

    claims = get_jwt_claims()
    user_id = claims.get('user_id')
    
    if not user_id:
        return jsonify({'message': 'Missing user_id in Token'}), 400

    if request.method == 'GET':
        return getUserTodo(note_id, user_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        note_description = content['note_description'] if 'note_description' in content.keys() else ''
        completed = content['completed'] if 'completed' in content.keys() else False
        return updateUserTodo(note_id, note_description, completed, user_id)

    if request.method == 'DELETE':
        return deleteUserTodo(note_id, user_id)
