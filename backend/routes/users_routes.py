from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..'))
sys.path.append(project_root)

from controllers.user import Users

users = Users()
users_bp = Blueprint('users', __name__, url_prefix='/api/users/')

@users_bp.route('/register', methods=['POST'], strict_slashes=False)
def create_user():
    try:
        data = request.get_json()
        response = users.create_user(data)
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

@users_bp.route('all', methods=['GET'], strict_slashes=False)
@jwt_required()
def list_all_users():
    try:
        response = users.list_all_users()
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500
    
@users_bp.route('dept/<dept_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def list_users_in_dept(dept_id):
    try:
        response = users.list_users_in_dept(dept_id)
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@users_bp.route('/type/update/<user_id>', methods=['POST'], strict_slashes=False)
@jwt_required()
def update_user_type(user_id):
    try:
        data = request.get_json()
        user_type = data.get('user_type')
        response = users.change_user_type(user_id, user_type)
        return response 
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

@users_bp.route('delete_user', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_user():
    try:
        data = request.get_json()
        response = users.delete_user(data)
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"})

