from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd
from ..database import get_db
from ..models import Employee
from ..auth.dependencies import get_current_user
import io

router = APIRouter()


@router.post("/upload-salary", summary="Upload salary excel file")
async def upload_salary(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Read file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), header=2)

        # Clean column names properly
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
        )

        print("CLEANED COLUMNS:", list(df.columns))

        processed = []
        skipped_no_epf = []
        missing_email = []

        for _, row in df.iterrows():

            # Skip empty rows
            if pd.isna(row.get("emp_id")):
                continue

            emp_id = str(row["emp_id"]).strip()

            # Safe EPF extraction
            pf = float(row.get("epf_@_12%", 0))

            # Rule 1: Skip if EPF <= 0
            if pf <= 0:
                skipped_no_epf.append(emp_id)
                continue

            # Rule 2: Fetch employee email from DB
            employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()

            if not employee or not employee.email:
                missing_email.append(emp_id)
                continue

            processed.append({
                "emp_id": emp_id,
                "email": employee.email,
                "basic": round(float(row.get("basic_+_da", 0)), 2),
                "hra": round(float(row.get("hra", 0)), 2),
                "net_pay": round(float(row.get("net_pay", 0)), 2),
                "pf": pf
            })

        return {
            "total_rows": len(df),
            "eligible_for_payslip": len(processed),
            "skipped_no_epf": skipped_no_epf,
            "missing_email": missing_email,
            "processed_employees": processed
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
