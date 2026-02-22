from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import Employee
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    total_active = db.query(Employee).filter(
        Employee.is_active == True
    ).count()

    total_inactive = db.query(Employee).filter(
        Employee.is_active == False
    ).count()

    recent_activity = [
        f"Welcome {current_user.email}",
        f"Dashboard viewed on {datetime.now().strftime('%d-%m-%Y')}",
        f"Total Active Employees: {total_active}",
        
    ]

    return {
        "total_active_employees": total_active,
        "recent_activity": recent_activity
    }