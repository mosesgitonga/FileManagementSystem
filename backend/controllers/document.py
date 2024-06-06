from datetime import datetime
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid

from models.models import Document, User
from models.engine.db_storage import DBStorage

class Documents:
    def __init__(self):
        self.storage = DBStorage()
        self.UPLOAD_FOLDER = './uploads/files/'
        self.ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'jpeg', 'gif', 'webp', 'docx',
                        'xlsx', 'pptx', 'rtf', 'png', 'bmp', 'wav', 'ogg',
                        'zip', 'tar.gz', 'rar'}

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def upload_file(self):
        try:
            if 'file' not in request.files:
                return jsonify({"message": "No file part"}), 400
            file = request.files['file']
            desired_filename = request.form.get('filename', file.filename)
            description = request.form.get('description')

            # Get the ID of the current user
            current_user_id = get_jwt_identity()
            user = self.storage.get(User, id=current_user_id)
            name = f"{user.first_name} {user.second_name}"

            if file.filename == '':
                return jsonify({"message": "No selected file"}), 400
            if file and self.allowed_file(file.filename):
                # Generate a unique filename to avoid conflicts
                if desired_filename:
                    file_ext = os.path.splitext(file.filename)[1]
                    filename = secure_filename(desired_filename)
                    filename = f"{filename}{file_ext}"
                else:
                    filename = secure_filename(file.filename)
                    filename = self.generate_unique_filename(filename)

                file_path = os.path.join(self.UPLOAD_FOLDER, filename)
                file.save(file_path)  # Saves file to UPLOAD_FOLDER

                # Create a new Document instance
                new_document = Document(
                    filename=filename,
                    description=description,
                    filepath=file_path,
                    uploaded_by=user.id,
                    current_department_id=user.department_id,
                )
                
                self.storage.new(new_document)
                self.storage.save()
                self.storage.close()

                return jsonify({"message": "File uploaded successfully"}), 200
            else:
                return jsonify({"message": "File type not allowed"}), 400
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal server error"}), 500

    def generate_unique_filename(self, filename):
        """
        Generates a unique filename to avoid conflicts.

        Args:
        - filename (str): The original filename.

        Returns:
        - str: A unique filename with the original file extension.
        """
        # Get the file extension
        file_ext = os.path.splitext(filename)[1]
        
        # Generate a unique identifier
        unique_id = uuid.uuid4().hex[:6]

        # Concatenate unique identifier with original filename (without extension)
        unique_filename = secure_filename(os.path.splitext(filename)[0] + '_' + unique_id) + file_ext

        return unique_filename

    def get_documents(self):
        """
        Gets all documents
        """
        try:
            documents = self.storage.get(Document)  
            document_list = [
                {
                    "id": doc.id,
                    "filename": doc.filename,
                    "description": doc.description,
                    "uploaded_by": doc.uploaded_by,
                    "created_at": doc.created_at,
                    "filepath": doc.filepath
                } for doc in documents
            ]
            return jsonify(document_list), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500