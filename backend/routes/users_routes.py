from flask import Flask, Blueprint, request, jsonify
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..'))
sys.path.append(project_root)

from controllers.user import Users

users = Users()
users_bp = Blueprint('users', __name__, url_prefix='/api/users/')

@users_bp.route('/create', methods=['POST'], strict_slashes=False)
def create_user():
    try:
        data = request.get_json()
        response = users.create_user(data)
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

@users_bp.route('list_all', methods=['GET'], strict_slashes=False)
def list_all_users():
    try:
        response = users.list_all_users()
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500
    
@users_bp.route('list_users_dept', methods=['GET'], strict_slashes=False)
def list_users_in_dept():
    try:
        data = request.get_json()
        response = users.list_users_in_dept(data)
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

