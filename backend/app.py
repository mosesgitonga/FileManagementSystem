from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt
from flask_redis import FlaskRedis
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta
from flask_socketio import SocketIO, emit
import shutil
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..'))
sys.path.append(project_root)

from models.engine.db_storage import DBStorage
from models.models import Document, User

# Initialize storage
storage = DBStorage()

load_dotenv()

app = Flask(__name__)
CORS(app)
# Load JWT secret key
jwt_secret_key = os.getenv('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# Configure Redis
app.config['REDIS_URL'] = "redis://localhost:6379/0"

# Set token expiration
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=365*15)  # Access token expires in 15 years
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=30)  # Refresh token expires in 30 minutes

# Initialize JWT and Redis
jwt = JWTManager(app)
redis_store = FlaskRedis(app)

# Check if a token is in the blacklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token_in_redis = redis_store.get(jti)
    return token_in_redis is not None

# Handle revoked tokens
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "Token has been revoked"}), 401

# Import and define blueprints
from routes.users_routes import users_bp
from routes.departments_routes import dept_bp
from routes.auth_routes import auth_bp
from routes.doc_route import doc_bp

# Define user logout route before registering the blueprint
@auth_bp.route('user/logout', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def logout():
    try:
        jti = get_jwt()['jti']  # JWT ID, a unique identifier for the token
        redis_store.set(jti, 'revoked', ex=3600)  # Token will be revoked for 1 hour (3600 seconds)
        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

# Register blueprints
app.register_blueprint(users_bp)
app.register_blueprint(dept_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(doc_bp)

# Initialize SocketIO
socketio = SocketIO(app)

# Document sharing route
@app.route('/api/docs/share', methods=['POST'], strict_slashes=False)
@jwt_required()
def share_document():
    data = request.get_json()
    document_id = data.get('document_id')
    to_department_id = data.get('to_department_id')

    try:
        document = storage.get(Document, document_id)
        if not document:
            return jsonify({"message": "Document not found"}), 404
        
        current_user_id = get_jwt_identity()
        user = storage.get(User, current_user_id)

        if document.current_department_id != user.department_id:
            return jsonify({"message": "Unauthorized"}), 403

        original_file_path = document.filepath
        file_name, file_ext = os.path.splitext(document.filename)
        new_file_name = f"{file_name}_{to_department_id}{file_ext}"
        new_file_path = os.path.join('./uploads/files/', new_file_name)
        
        shutil.copy2(original_file_path, new_file_path)

        new_document = Document(
            filename=new_file_name,
            description=document.description,
            filepath=new_file_path,
            uploaded_by=document.uploaded_by,
            current_department_id=to_department_id
        )
        
        storage.new(new_document)
        storage.save()

        # Notify the frontend about the new document
        socketio.emit('document_shared', {'department_id': to_department_id, 'document': new_document.to_dict()})

        return jsonify({"message": "Document shared successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

if __name__ == "__main__":
    try:
        redis_store.ping()
        print("Redis is running and connected!")
    except redis.ConnectionError:
        print("Redis is not running or cannot be connected to.")
        exit(1)

    socketio.run(app, debug=True)
