from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token
import bcrypt
from models.models import User
from models.engine.db_storage import DBStorage
from controllers.user import Users

storage = DBStorage()
users = Users()
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/user/register', methods=['POST'], strict_slashes=False)
def register_user():
    try:
        data = request.get_json()
        response = users.create_user(data)
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

@auth_bp.route('/user/login', methods=['POST'], strict_slashes=False)
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Get user by email
        user = storage.get(User, email=email)
        if not user:
            return jsonify({"error": "No user with that email"}), 401
        
        # Check password
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200
        else:
            return jsonify({"message": "Unauthorized, check password or email"}), 401
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"})

@auth_bp.route('/refresh', methods=['POST'], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        return jsonify(access_token=new_access_token), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500