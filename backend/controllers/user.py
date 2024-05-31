from flask import jsonify
from models.models import User
from models.engine.db_storage import DBStorage
import json
import uuid
class Users:
    """
    Users class to handle operations related to User management.
    """

    def __init__(self):
        """
        Initializes the Users class.
        """
        self.storage = DBStorage()

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
        existing_users = self.storage.get(User)

        # Check if there are any users in the database
        if not existing_users:
            user_type = 'admin'  # First user becomes admin
        else:
            user_type = 'member' # rest of the users become members unless promoted by admin
        
        #check if employee id exists to make sure it is unique
        existing_employee_id = self.storage.get(User, employee_id=employee_id)
        if existing_employee_id:
            print('employee id already exists')
            return jsonify({"message": "Employee id already exists"})

        new_user = User(
            id=uuid.uuid4(),
            first_name=first_name,
            second_name=second_name,
            employee_id=employee_id,
            user_type=user_type
        )
        try:
            self.storage.new(new_user)
            self.storage.save()
            return jsonify({"message": "User created successfully."}), 201
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

    def list_all_users(self):
        """
        Lists all users in the database.
        
        Returns:
        Response: JSON response containing a list of all users.
        """
        try:
            users = self.storage.get(User)
            jsonified_users = [user.to_dict() for user in users]
            return jsonify({"users": jsonified_users})
        except Exception as e:
            return jsonify({"message": str(e)}), 500

    def list_users_in_dept(self, data):
        """
        Lists all users in a certain department.
        
        Parameters:
        department_id (str): The ID of the department to filter users by.
        
        Returns:
        Response: JSON response containing a list of users in the specified department.
        """
        try:
            department_id = data.get('department_id')
            users = self.storage.get(User).filter_by(department_id=department_id).all()
            jsonified_users = [user.to_dict() for user in users]
            return jsonify({"users": jsonified_users})
        except Exception as e:
            return jsonify({"message": str(e)}), 500

    def change_user_type(self, user_id, user_type):
        """
        Changes the user type, e.g., from admin to member or from member to admin.
        
        Parameters:
        user_id (str): The ID of the user whose type is to be changed.
        user_type (str): The new user type.
        
        Returns:
        Response: JSON response indicating success or failure of the operation.
        """
        if not user_id:
            print('Expected user_id to be passed in the class method parameters.')
            return jsonify({"message": "User ID is required."}), 400

        try:
            user = self.storage.get(User, id=user_id)
            if user is None:
                return jsonify({"message": "User not found."}), 404

            user.user_type = user_type
            self.storage.new(user)
            self.storage.save()
            return jsonify({"message": "User type changed successfully."}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

    def delete_user(self, user_id):
        """
        Deletes a user by their ID.
        
        Parameters:
        user_id (str): The ID of the user to be deleted.
        
        Returns:
        Response: JSON response indicating success or failure of the operation.
        """
        try:
            user = self.storage.get(User, id=user_id)
            if user is None:
                return jsonify({"message": "User not found."}), 404

            self.storage.delete(user)
            self.storage.save()
            return jsonify({"message": "User deleted successfully."}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500
