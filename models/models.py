from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base_model import Base, BaseModel

"""
Structure of the model where obtained data will be stored
"""

class User(Base, BaseModel):
    __tablename__ = "users"  # Name of the table will be users
    first_name = Column(String(90), nullable=False)
    second_name = Column(String(90), nullable=False)
    employee_id = Column(String(100), unique=True, nullable=False)  # id could be a string eg: 'A123', 'B234'
    user_type = Column(String(100), nullable=False)  # [admin, member]

    department_id = Column(String(120), ForeignKey('departments.id'), nullable=False)
    department = relationship("Department", back_populates="users")


class Department(Base, BaseModel):
    __tablename__ = "departments"
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(300), nullable=True)
    
    users = relationship("User", back_populates="department")
    documents = relationship("Document", back_populates="department")


class Document(Base, BaseModel):
    __tablename__ = "documents"
    filename = Column(String(120), nullable=False)
    filepath = Column(String(180), nullable=False)
    uploaded_by = Column(String(120), ForeignKey('users.id'), nullable=False)
    current_department_id = Column(String(120), ForeignKey('departments.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user = relationship("User")
    department = relationship("Department", back_populates="documents")


class DocumentTransfer(Base, BaseModel):
    __tablename__ = 'document_transfers'
    document_id = Column(String(120), ForeignKey('documents.id'), nullable=False)
    from_department_id = Column(String(120), ForeignKey('departments.id'), nullable=False)
    to_department_id = Column(String(120), ForeignKey('departments.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    document = relationship("Document")
    from_department = relationship("Department", foreign_keys=[from_department_id])
    to_department = relationship("Department", foreign_keys=[to_department_id])
