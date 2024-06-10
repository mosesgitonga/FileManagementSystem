from datetime import datetime
from flask import jsonify, request, send_file, current_app
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid

from models.models import Document, User
from models.engine.db_storage import DBStorage

class Documents:
    def __init__(self):
        self.storage = DBStorage()
        self.UPLOAD_FOLDER = 'uploads/files/'
        self.ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'jpeg', 'gif', 'webp', 'docx',
                        'xlsx', 'pptx', 'rtf', 'png', 'bmp', 'wav', 'ogg',
                        'zip', 'tar.gz', 'rar', 'odg'}

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def upload_file(self):
        try:
            current_user_id = get_jwt_identity()
            user = self.storage.get(User, id=current_user_id)
            if not user.department_id:
                print('Unauthorized, you dont belong to any department')
                return jsonify({"message": "Unauthorized, you don't belong to any department"})

            if 'file' not in request.files:
                return jsonify({"message": "No file part"}), 400
            file = request.files['file']
            desired_filename = request.form.get('filename', file.filename)
            description = request.form.get('description')

            
            name = f"{user.first_name} {user.second_name}"

            if file.filename == '':
                return jsonify({"message": "No selected file"}), 400
            if file and self.allowed_file(file.filename):
                if desired_filename:
                    file_ext = os.path.splitext(file.filename)[1]
                    if not os.path.splitext(desired_filename)[1]:
                        filename = secure_filename(desired_filename) + file_ext
                    else:
                        filename = secure_filename(desired_filename)
                else:
                    filename = secure_filename(file.filename)
                    filename = self.generate_unique_filename(filename)

                file_path = os.path.join(self.UPLOAD_FOLDER, filename)
                file.save(file_path)

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
            current_app.logger.error(e)
            return jsonify({"error": "Internal server error"}), 500

    def generate_unique_filename(self, filename):
        file_ext = os.path.splitext(filename)[1]
        unique_id = uuid.uuid4().hex[:6]
        unique_filename = secure_filename(os.path.splitext(filename)[0] + '_' + unique_id) + file_ext
        return unique_filename

    def get_documents(self):
        try:
            """returns all documents in the user current department
            """
            current_user_id = get_jwt_identity()
            current_user_dept_id = self.storage.get(User, id=current_user_id).department_id
            docs = self.storage.get(Document, current_department_id=current_user_dept_id)
            document_list = [
                {
                    "id": doc.id,
                    "filename": doc.filename,
                    "description": doc.description,
                    "uploaded_by": doc.uploaded_by,
                    "created_at": doc.created_at,
                    "filepath": doc.filepath
                } for doc in docs
            ]
            return jsonify(document_list), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

    def download_doc(self, filename):
        try:
            # Get the absolute path to the upload folder
            upload_folder_abs_path = os.path.abspath(self.UPLOAD_FOLDER)
            file_path = os.path.join(upload_folder_abs_path, filename)
            current_app.logger.debug(f"Attempting to download file from: {file_path}")

            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
            else:
                current_app.logger.error(f"File not found: {file_path}")
                return jsonify({"message": "File not found"}), 404
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({"message": "Internal server error"}), 500