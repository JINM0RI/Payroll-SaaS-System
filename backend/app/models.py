from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True)
    password_hash = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(String(50), unique=True, index=True)
    name = Column(String(150))
    email = Column(String(150))
    created_at = Column(TIMESTAMP, server_default=func.now())


class Payslip(Base):
    __tablename__ = "payslips"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(String(50))
    file_path = Column(Text)
    status = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now())


class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(String(50))
    email = Column(String(150))
    status = Column(String(20))
    error_message = Column(Text)
    sent_at = Column(TIMESTAMP, server_default=func.now())
