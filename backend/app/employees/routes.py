from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeResponse
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
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    # Fetch employee
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Soft delete by marking inactive
    employee.is_active = False

    db.commit()
    return {"message": f"Employee {employee.name} deleted successfully"}
