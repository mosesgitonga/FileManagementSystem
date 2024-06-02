from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from flask_redis import FlaskRedis
from dotenv import load_dotenv
from datetime import timedelta
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..'))
sys.path.append(project_root)

#from models.engine.db_storage import DBStorage


load_dotenv()

app = Flask(__name__)

jwt_secret_key = os.getenv('JWT_SECRET_KEY')

app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.config['REDIS_URL'] = "redis://localhost:6379/0"


# Set token expiration
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=365*15)  # Access token expires in 15 minutes
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=30)    # Refresh token expires in 30 days


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

from routes.users_routes import users_bp
from routes.departments_routes import dept_bp
from routes.auth_routes import auth_bp
from routes.doc_route import doc_bp

@auth_bp.route('user/logout', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def logout():
    try:
        jti = get_jwt()['jti']  # JWT ID, a unique identifier for the token
        redis_store.set(jti, 'revoked', ex=3600)  # Token will be revoked for 1 hour (3600 seconds)
        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"})

app.register_blueprint(users_bp)
app.register_blueprint(dept_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(doc_bp)

if __name__ == "__main__":
    try:
        redis_store.ping()
        print("Redis is running and connected!")
    except redis.ConnectionError:
        print("Redis is not running or cannot be connected to.")
        exit(1)

    app.run(debug=True)
