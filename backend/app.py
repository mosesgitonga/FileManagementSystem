from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..'))
sys.path.append(project_root)

#from models.engine.db_storage import DBStorage
from routes.users_routes import users_bp
from routes.departments_routes import dept_bp


load_dotenv()

app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(dept_bp)

jwt_secret_key = os.getenv('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = jwt_secret_key
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True)
