from models.engine.db_storage import DBStorage
from models.models import Document, User
from flask_jwt_extended import get_jwt_identity
from flask import request, jsonify
import shutil
import os

"""
sharing document
"""

class Share:
    def __init__(self):
        self.storage = DBStorage()

    def share_document(self):
        data = request.get_json()
        doc_id = data.get('document_id')
        dest_dept_id = data.get('dest_dept_id')
        try:
            current_user_id = get_jwt_identity()
            current_user = self.storage.get(User, id=current_user_id)
            source_dept_id = current_user_id.department_id

            document = storage.get(Document, doc_id)
            if not document:
                return jsonify({"message": "Document not found"}), 404

            if document.current_department_id != current_user.department_id:
                return jsonify({"message": "Internal server error"})
            
            original_file_path = document.filepath
            file_name, file_ext = os.path.splitext(document.filename)
            new_filename = f"{file_name}cp{file_ext}"
            new_file_path = os.path.join('./uploads/files/', new_filename)

            shutil.copy2(original_file_path, new_file_path)  # Copy the file

             # Create a new Document entry for the copied file
            new_document = Document(
                filename=new_filename,
                description=document.description,
                filepath=new_file_path,
                uploaded_by=document.uploaded_by,
                current_department_id=current_user.to_department_id
            )

            self.storage.new(new_document)
            self.save()
            
            shared_documents = DocumentTransfer(
                document_id=document_current_id,
                from_department_id=current_department_id,
                to_department_id=dest_dept_id
            )
            
            self.storage.new(shared_documents)
            self.storage.save()
            self.storage.close()
            return jsonify({"message": "Document shared successfully"})
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"})

