#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os

from models.base_model import Base
from models.models import User, Department, Document, DocumentTransfer

# loads enviroment variables from the .env file
load_dotenv()

class DBStorage:
    __session = None
    __engine = None

    def __init__(self):
        """Initializes the DBStorage instance"""
        self.db_URI = getenv('SQLALCHEMY_DATABASE_URI')
        print(f"Database URI: {self.db_URI}")
        if not self.db_URI:
            raise ValueError("No SQLALCHEMY_DATABASE_URI environment variable set")
        self.__engine = create_engine(self.db_URI, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
        self.reload()
 
    def new(self, obj) -> None:
        """Adds the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session."""
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def delete(self, obj=None) -> None:
        """Deletes an object from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self) -> None:
        """Reloads the data in the database."""
        print("Creating tables if they don't exist...")
        try:
            Base.metadata.create_all(self.__engine)
            print("Tables created.")
        except Exception as e:
            print(f"Error creating tables: {e}")
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def query(self, model):
        """
        returns query object for the specified object
        """
        return self.__session.query(model)

    def get(self, cls=None, **kwargs):
        """Returns an object based on the class and key."""
        if not cls:
            return None

        if not kwargs:
            return self.__session.query(cls).all()

        if 'id' in kwargs:
            return self.__session.query(cls).filter_by(id=kwargs['id']).first()

        if 'email' in kwargs:
            return self.__session.query(cls).filter_by(email=kwargs['email']).first()

        return self.__session.query(cls).filter_by(**kwargs).all()

    def close(self):
        """Closes the current session."""
        self.__session.remove()
