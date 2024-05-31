from flask import Flask
import os
import sys
current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..'))
sys.path.append(project_root)

#from models.engine.db_storage import DBStorage
from routes.users_routes import users_bp

#storage = DBStorage()
#storage.reload()

app = Flask(__name__)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)
