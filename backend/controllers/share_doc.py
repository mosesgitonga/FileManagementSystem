from models.engine.db_storage import DBStorage
from models.models import Document, User, DocumentTransfer
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request, jsonify
import random
import shutil
import os

class Share:
    def __init__(self):
        self.storage = DBStorage()

    @jwt_required()
    def share_document(self, doc_id, dest_dept_id):
        try:
            current_user_id = get_jwt_identity()
            current_user = self.storage.get(User, id=current_user_id)
            
            if not current_user:
                return jsonify({"message": "User not found"}), 404
            
            document = self.storage.get(Document, id=doc_id)
            if not document:
                return jsonify({"message": "Document not found"}), 404

            if document.current_department_id != current_user.department_id:
                return jsonify({"message": "Unauthorized"}), 403
            

            original_file_path = document.filepath
            file_name, file_ext = os.path.splitext(document.filename)
            random_nums = random.randrange(0, 120)
            new_filename = f"{file_name}_{random_nums}{file_ext}"
            new_file_path = os.path.join('./uploads/files/', new_filename)

            # Copy the file
            shutil.copy2(original_file_path, new_file_path)

            # Create a new Document entry for the copied file
            new_document = Document(
                filename=new_filename,
                description=document.description,
                filepath=new_file_path,
                uploaded_by=document.uploaded_by,
                current_department_id=dest_dept_id  
            )

            self.storage.new(new_document)
            self.storage.save()

            # Record the document transfer
            shared_documents = DocumentTransfer(
                document_id=document.id,
                from_department_id=current_user.department_id,
                to_department_id=dest_dept_id
            )

            self.storage.new(shared_documents)
            self.storage.save()

            return jsonify({"message": "Document shared successfully"})
        
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500
        
        finally:
            self.storage.close()
