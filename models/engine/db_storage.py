#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from base_model import Base

load_dotenv()

class DBStorage:
    __session = None
    __engine = None

    def __init__(self):
        self.db_URI = getenv('SQLALCHEMY_DATABASE_URI')
        if not self.db_URI:
            raise ValueError("No SQLALCHEMY_DATABASE_URI environment variable set")
        self.__engine = create_engine(self.db_URI)
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
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls=None, **kwargs):
        """Returns an object based on the class and key."""
        if not cls:
            return None

        if not kwargs:
            return self.__session.query(cls).all()

        if 'id' in kwargs:
            return self.__session.query(cls).filter_by(id=kwargs['id']).first()
        
        return self.__session.query(cls).filter_by(**kwargs).first()

    def close(self):
        """Closes the current session."""
        self.__session.remove()
