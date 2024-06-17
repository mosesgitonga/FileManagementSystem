from models.models import Document, User, Department
from models.engine.db_storage import DBStorage 
from flask_jwt_extended import get_jwt_identity
from flask import request, jsonify
from sqlalchemy import or_

class Search:
    def __init__(self):
        self.storage = DBStorage()

    def searchDocsInDept(self):
        """
        searches for docs in a departments
        """
        try:
            current_user_id = get_jwt_identity()
            current_user = self.storage.get(User, id=current_user_id)
            current_user_department = current_user.department

            query = request.args.get('query', '')

            # Perform the search query within the department
            results = self.storage.query(Document).filter(
                Document.current_department_id == current_user_department.id,
                or_(
                    Document.filename.ilike(f'%{query}%'),
                    Document.description.ilike(f'%{query}%'),
                    Document.created_at.ilike(f'%{query}%')
                )
            ).all()
            results_list = [
                {
                "id": doc.id,
                "filename": doc.filename,
                "description": doc.description,
                "uploaded_by": doc.uploaded_by,
                "created_at": doc.created_at,
                "updated_at": doc.updated_at
                } for doc in results
            ]
            return jsonify(results_list)
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal server error"})
