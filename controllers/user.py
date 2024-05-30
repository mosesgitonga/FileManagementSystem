from flask import jsonify
from models.models import User
from models import storage
import json

class Users:
    """
    Users class to handle operations related to User management.
    """

    def __init__(self):
        """
        Initializes the Users class.
        """
        pass

    def create_user(self, data):
        """
        Creates a new user and adds it to the database.
        
        Parameters:
        data (dict): A dictionary containing user details with keys
                     'first_name', 'second_name', 'employee_id', and 'user_type'.
        
        Returns:
        Response: JSON response indicating success or failure of the operation.
        """
        first_name = data.get('first_name')
        second_name = data.get('second_name')
        employee_id = data.get('employee_id')
        user_type = data.get('user_type')

        # Validate whether user type exists
        user_types = ['admin', 'member']
        if user_type not in user_types:
            return jsonify({"message": "Invalid user type."}), 400

        new_user = User(
            first_name=first_name,
            second_name=second_name,
            employee_id=employee_id,
            user_type=user_type
        )
        try:
            storage.new(new_user)
            storage.save()
            return jsonify({"message": "User created successfully."}), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 500

    def list_all_users(self):
        """
        Lists all users in the database.
        
        Returns:
        Response: JSON response containing a list of all users.
        """
        try:
            users = storage.get(User).all()
            jsonified_users = [user.to_dict() for user in users]
            return jsonify({"users": jsonified_users})
        except Exception as e:
            return jsonify({"message": str(e)}), 500

    def list_users_in_dept(self, department_id):
        """
        Lists all users in a certain department.
        
        Parameters:
        department_id (str): The ID of the department to filter users by.
        
        Returns:
        Response: JSON response containing a list of users in the specified department.
        """
        try:
            users = storage.get(User).filter_by(id=department_id).all()
            jsonified_users = [user.to_dict() for user in users]
            return jsonify({"users": jsonified_users})
        except Exception as e:
            return jsonify({"message": str(e)}), 500

    # def change_user_type(self):
