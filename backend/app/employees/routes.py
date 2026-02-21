from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Employee, User
from app.schemas import EmployeeCreate, EmployeeResponse, EmployeeDelete
from app.auth.dependencies import get_current_user
from app.auth.utils import verify_password
from sqlalchemy import func

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# Get all employees
@router.get("/", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    # Only fetch employees where is_active is True
    return db.query(Employee).filter(Employee.is_active == True).all()


# Add employee
@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):

    # Count existing employees
    count = db.query(func.count(Employee.id)).scalar()

    # Generate emp_id like EMP001, EMP002, etc.
    new_emp_id = f"EMP{str(count + 1).zfill(3)}"

    new_employee = Employee(
        emp_id=new_emp_id,
        name=employee.name,
        email=employee.email
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    data: EmployeeDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 🔐 Step 1 — Verify password from users table
    if not verify_password(data.password, current_user.password_hash):
        raise HTTPException(status_code=403, detail="Invalid password")

    # Step 2 — Find employee
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Step 3 — Soft delete
    employee.is_active = False
    employee.deleted_at = func.now()
    employee.deleted_by = current_user.id

    db.commit()

    return {"message": "Employee deleted successfully"}
