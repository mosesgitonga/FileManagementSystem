from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..'))
sys.path.append(project_root)

from controllers.document import Documents

documents = Documents()
doc_bp = Blueprint('docs', __name__, url_prefix='/api/docs')

@doc_bp.route('upload', methods=['POST'], strict_slashes=False)
@jwt_required()
def upload_file():
    try:
        response = documents.upload_file()
        return response 
    except Exception as e:
        print(e)
        return jsonify({"message": "Error Internal server error"})