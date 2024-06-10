from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required

from controllers.search import Search
search_bp = Blueprint('search', __name__, url_prefix='/api/search')

search = Search()

@search_bp.route('/dept/docs', methods=['GET'], strict_slashes=False)
@jwt_required()
def search_docs_in_dept():
    try:
        response = search.searchDocsInDept()
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"})
