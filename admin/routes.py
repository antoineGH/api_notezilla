from flask import request, Blueprint, jsonify, render_template
from flask_jwt_extended import jwt_required
from admin.utils import deleteTodo
from admin.utils import isAdmin, getUsers, postUser, getUser, updateUser, deleteUser, getTodos, postTodo, getTodo, updateTodo, deleteTodo, getTodosUser

admin = Blueprint('admin', __name__)

@admin.route('/')
def home():
    return render_template('documentation.html', title='Documentation')

@admin.route('/api/admin/users', methods=['GET', 'POST'])
@jwt_required
def adminUsers():
    if not isAdmin():
        return jsonify({'message': "Unauthorized Admin only"}), 403 
    if request.method == 'GET':
        return getUsers()
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        email = content.get("email", None)
        password = content.get("password", None)
        first_name = content.get("first_name", None)
        last_name = content.get("last_name", None)
        if not email: 
            return jsonify({"message": 'Missing email in JSON'})
        if not password: 
            return jsonify({"message": 'Missing password in JSON'})
        if not first_name: 
            return jsonify({"message": 'Missing first name in JSON'})
        if not last_name: 
            return jsonify({"message": 'Missing last name in JSON'})
        return postUser(email, password, first_name, last_name)

@admin.route('/api/admin/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE']) 
@jwt_required
def adminUser(user_id):
    if not isAdmin():
        return jsonify({'message': "Unauthorized Admin only"}), 403 

    if not user_id:
        return jsonify({"message": "Missing user_id in request"}), 404

    if request.method == 'GET':
        return getUser(user_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        email = content['email'] if 'email' in content.keys() else ''
        password = content['password'] if 'password' in content.keys() else ''
        first_name = content['first_name'] if 'first_name' in content.keys() else ''
        last_name = content['last_name'] if 'last_name' in content.keys() else ''
        return updateUser(user_id, email, password, first_name, last_name)

    if request.method == 'DELETE':
        return deleteUser(user_id)

@admin.route('/api/admin/notes', methods=['GET', 'POST'])
@jwt_required
def notes():
    if not isAdmin():
        return jsonify({'message': "Unauthorized Admin only"}), 403 

    if request.method == 'GET':
        return getTodos()
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        note_description = content.get("note_description", None)
        completed = content.get("completed", None)
        user_id = content.get("user_id", None)
        if not note_description: 
            return jsonify({"message": 'Missing note_description in JSON'})
        if not completed: 
            return jsonify({"message": 'Missing completed in JSON'})
        if not user_id: 
            return jsonify({"message": 'Missing user_id in JSON'})
        return postTodo(note_description, completed, user_id)

@admin.route('/api/admin/note/<int:note_id>', methods=['GET', 'PUT', 'DELETE']) 
@jwt_required
def note(note_id):
    if not isAdmin():
        return jsonify({'message': "Unauthorized Admin only"}), 403 

    if not note_id:
        return jsonify({"message": "Missing note_id in request"}), 404

    if request.method == 'GET':
        return getTodo(note_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        note_description = content['note_description'] if 'note_description' in content.keys() else ''
        completed = content['completed'] if 'completed' in content.keys() else ''
        user_id = content['user_id'] if 'user_id' in content.keys() else ''
        return updateTodo(note_id, note_description, completed, user_id)

    if request.method == 'DELETE':
        return deleteTodo(note_id)

@admin.route('/api/admin/note/user/<int:user_id>', methods=['GET'])
@jwt_required
def notesUser(user_id):
    if not isAdmin():
        return jsonify({'message': "Unauthorized Admin only"}), 403 

    if not user_id:
        return jsonify({"message": "Missing user_id in request"}), 404
    return getTodosUser(user_id)
