from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from dotenv import load_dotenv
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..'))
sys.path.append(project_root)

#from models.engine.db_storage import DBStorage
from routes.users_routes import users_bp
from routes.departments_routes import dept_bp
from routes.auth_routes import auth_bp

load_dotenv()

app = Flask(__name__)

app.register_blueprint(users_bp)
app.register_blueprint(dept_bp)
app.register_blueprint(auth_bp)

jwt_secret_key = os.getenv('JWT_SECRET_KEY')

app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.config['REDIS_URL'] = "redis://localhost:6379/0"

jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True)
