from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from scratch.utils import deleteUserScratch, getUserScratch, postUserScratch, deleteUserScratch

scratch = Blueprint('scratch', __name__)

@scratch.route('/api/scratch', methods=['GET', 'POST', 'DELETE'])
@jwt_required
def userScratch():
    claims = get_jwt_claims()
    user_id = claims.get('user_id')
    
    if not user_id:
        return jsonify({'message': 'Missing user_id in Token'}), 400
    
    if request.method == 'GET':
        return getUserScratch(user_id)

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        scratch_title = content.get("scratch_title", None)
        scratch_content = content.get("scratch_content", None)
        completed = content.get("completed", None)
        return postUserScratch(scratch_title, scratch_content, completed, user_id)

    if request.method == 'DELETE':
        return deleteUserScratch(user_id)
