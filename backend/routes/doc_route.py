from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..'))
sys.path.append(project_root)

from controllers.document import Documents
from controllers.share_doc import Share

share = Share()
documents = Documents()
doc_bp = Blueprint('docs', __name__, url_prefix='/api/docs')

@doc_bp.route('/upload', methods=['POST'], strict_slashes=False)
@jwt_required()
def upload_file():
    try:
        response = documents.upload_file()
        return response 
    except Exception as e:
        print(e)
        return jsonify({"message": "Error Internal server error"}), 500

@doc_bp.route('/all', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_docs():
    """returns all documents in the user current department
    """
    try:
        response = documents.get_documents()
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

@doc_bp.route('/download/<filename>', methods=['GET'], strict_slashes=False)
@jwt_required()
def download(filename):
    try:
        response = documents.download_doc(filename)
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

@doc_bp.route('/share/<doc_id>/<dest_dept_id>', methods=['POST'], strict_slashes=False)
@jwt_required()
def share_doc(doc_id, dest_dept_id):
    try:
        response = share.share_document(doc_id, dest_dept_id)
        return response
    except Exception as e:
        print(e)
        return jsonify({"Error": "Internal server error"}), 500
