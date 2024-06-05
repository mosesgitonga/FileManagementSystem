from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from flask import jsonify
from models.models import Department, User
from models.engine.db_storage import DBStorage
import json

class Departments:
    """
    Departments class to handle operations related to Department management.
    """

    def __init__(self):
        """
        Initializes the Departments class.
        """
        self.storage = DBStorage()

    def create_dept(self, data):
        """
        Creates a new department and adds it to the database.
        
        Parameters:
        data (dict): A dictionary containing department details with keys
                     'name' and 'description'.
        
        Returns:
        Response: JSON response indicating success or failure of the operation.
        """
        try:
            admin_id = get_jwt_identity()
            # Verify the user is an admin
            user = self.storage.get(User, id=admin_id)
            if not user or user.user_type != 'admin':
                return jsonify({"message": "Unauthorized, contact admin"}), 403

            name = data['name']
            description = data.get('description', '')

            
            # Make sure the name does not exist 
            existing_dept = self.storage.get(Department, name=name)
            if existing_dept:
                return jsonify({"message": "Department name already exists"}), 400
        
            new_dept = Department(
                name=name,
                description=description
            )

            self.storage.new(new_dept)
            self.storage.save()
            user.department_id = new_dept.id
            self.storage.new(user)
            self.storage.save()
            self.storage.close()
            return jsonify({"message": "Department created successfully."}), 201
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

    def get_department_by_id(self, id):
        """
        Gets a single department using its ID.
        
        Parameters:
        id (str): The ID of the department to be retrieved.
        
        Returns:
        Response: JSON response containing the department details or an error message.
        """
        try:
            dept = self.storage.get(Department, id=id)
            if dept is None:
                return jsonify({"message": "Department not found."}), 404

            jsonified_dept = dept.to_dict()
            return jsonify({"dept": jsonified_dept}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

    def list_all_departments(self):
        """
        Lists all departments in the database.
        
        Returns:
        Response: JSON response containing a list of all departments.
        """
        try:
            depts = self.storage.get(Department)
            jsonified_depts = [dept.to_dict() for dept in depts]
            return jsonify(jsonified_depts), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

    def add_user_to_dept(self, dept_id, user_id):
        """
        adds user to a certain department
        """
        try:

            # get user from id
            user = self.storage.get(User, id=user_id)
            user.department_id = dept_id
            
            self.storage.new(user)
            self.storage.save()
            self.storage.close()
            return jsonify({"message": "user dept updated successfuly"})
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"})

    def change_dept_name(self, id, new_name):
        """
        Changes the name of a department.
        
        Parameters:
        id (str): The ID of the department whose department name is to be changed.
        new_name (str): The new name for the department.
        
        Returns:
        Response: JSON response indicating success or failure of the operation.
        """
        try:
            dept = self.storage.get(Department, id=id)
            if dept is None:
                return jsonify({"message": "Department not found."}), 404

            dept.name = new_name
            self.storage.new(dept)
            self.storage.save()
            return jsonify({"message": f"Department name has been changed to {dept.name}"}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

    def update_dept_description(self, id, new_description):
        """
        Updates the description of a department.
        
        Parameters:
        id (str): The ID of the department whose description is to be updated.
        new_description (str): The new description for the department.
        
        Returns:
        Response: JSON response indicating success or failure of the operation.
        """
        try:
            dept = self.storage.get(Department, id=id)
            if dept is None:
                return jsonify({"message": "Department not found."}), 404

            dept.description = new_description
            self.storage.new(dept)
            self.storage.save()
            return jsonify({"message": "Department description updated successfully."}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

    def delete_department(self, id):
        """
        Deletes a department by its ID.
        
        Parameters:
        id (str): The ID of the department to be deleted.
        
        Returns:
        Response: JSON response indicating success or failure of the operation.
        """
        try:
            dept = self.storage.get(Department, id=id)
            if dept is None:
                return jsonify({"message": "Department not found."}), 404

            self.storage.delete(dept)
            self.storage.save()
            return jsonify({"message": "Department has been deleted."}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500
 