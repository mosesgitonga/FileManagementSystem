#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import uuid

time_format = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()

class BaseModel(Base):
    """The BaseModel class from which future classes will be derived"""

    __abstract__ = True  # This class is meant to be inherited from, not instantiated directly

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        super().__init__(*args, **kwargs)
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if isinstance(self.created_at, str):
                self.created_at = datetime.strptime(self.created_at, time_format)
            if isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime(self.updated_at, time_format)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.to_dict())

    def save(self):
        """Updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance to dictionary for serialization"""
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = self.__class__.__name__
        dictionary["created_at"] = self.created_at.strftime(time_format)
        dictionary["updated_at"] = self.updated_at.strftime(time_format)
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]
        return dictionary
