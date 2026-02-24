from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True)
    password_hash = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    role = Column(String(50), default="user")



class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(String(50), unique=True, index=True)
    name = Column(String(150))
    email = Column(String(150), nullable=True)
    is_active = Column(Boolean, default=True) 
    

    
