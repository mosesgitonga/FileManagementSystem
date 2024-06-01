from flask import Flask, Blueprint, request, jsonify
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..'))
sys.path.append(project_root)

from controllers.department import Departments

departments = Departments()
dept_bp = Blueprint('dept', __name__, url_prefix='/api/dept/')

@dept_bp.route('/create', methods=['POST'], strict_slashes=False)
def create_dept():
    try:
        data = request.get_json()
        response = departments.create_dept(data)
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

@dept_bp.route('get/<id>', methods=['GET'], strict_slashes=False)
def get_department(id):
    try:
        response = departments.get_department_by_id(id)   
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"})
    
@dept_bp.route('list/all', methods=['GET'], strict_slashes=False)
def list_all():
    try:
        response = departments.list_all_departments()
        return response
    except Exception as e:
        return jsonify({"error": "Internal server error"})

@dept_bp.route('update/name/<id>', methods=['POST'], strict_slashes=False)
def update_dept_name(id):
    try:
        new_name = data['new_name'] = request.get('new_name')
        response = departments.change_dept_name(id, new_name)
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

@dept_bp.route('update/description/<id>', methods=['POST'], strict_slashes=False)
def update_description(id):
    try:
        data = request.get_json()
        new_description = data.get('description')
        response = departments.update_dept_description(id, new_description)
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500


@dept_bp.route('delete/<id>', methods=['POST'], strict_slashes=False)
def delete(id):
    try:
        response = departments.delete_department(id)
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

