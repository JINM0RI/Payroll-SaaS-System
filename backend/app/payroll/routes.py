import os
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd
from ..database import get_db
from ..models import Employee
from ..auth.dependencies import get_current_user
from ..utils.modern_payslip_generator import generate_modern_payslips
import zipfile
from fastapi.responses import FileResponse

import io

router = APIRouter()
import re
import calendar
from datetime import datetime

def extract_month_year_from_filename(filename):
    # Example: "Jan 26 Salary Statement Vanagaram.xlsx"
    
    match = re.search(r'([A-Za-z]{3})\s*(\d{2})', filename)

    if match:
        month_short = match.group(1).title()   # Jan
        year_short = int(match.group(2))       # 26
        
        # Convert 26 → 2026
        year_full = 2000 + year_short

        try:
            month_number = datetime.strptime(month_short, "%b").month
            month_name = calendar.month_name[month_number]
            return month_name, year_full
        except:
            pass

    # fallback to current date
    today = datetime.today()
    return today.strftime("%B"), today.year



@router.post("/upload-salary", summary="Upload salary excel file")
async def upload_salary(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:

        # STEP 1 — Save Uploaded File
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # STEP 2 — Extract Month & Year
        month_name, year = extract_month_year_from_filename(file.filename)

        # STEP 3 — Read Excel
        df = pd.read_excel(file_path, header=2)

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
        )

        processed = []
        skipped_no_epf = []
        missing_email = []

        def safe_float(value):
            if pd.isna(value):
                return 0
            return round(float(value), 2)


        # STEP 4 — Process Rows
        for _, row in df.iterrows():

            if pd.isna(row.get("emp_id")):
                continue

            emp_id = str(row["emp_id"]).strip()

            pf = pd.to_numeric(row.get("epf_@_12%"), errors="coerce")

            if pd.isna(pf) or pf <= 0:
                skipped_no_epf.append(emp_id)
                continue

            employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()

            if not employee or not employee.email:
                missing_email.append(emp_id)
                continue

            processed.append({
                "emp_id": emp_id,
                "name": row.get("name_of_employee", ""),
                "email": employee.email,
                "days_work": safe_float(row.get("days_work")),
                "basic": safe_float(row.get("basic_+_da")),
                "hra": safe_float(row.get("hra")),
                "ot_days": safe_float(row.get("ot_days")),  
                "gross_wages": safe_float(row.get("gross_wages")),
                "pf": safe_float(row.get("epf_@_12%")),
                "esi": safe_float(row.get("esi_@_0.75%")),
                "salary_adv": safe_float(row.get("salary_adv")),
                "net_pay": safe_float(row.get("net_pay")),
                "other_allowance": safe_float(row.get("other_allowance")),
                
            })

        # STEP 5 — Generate Payslips (ONLY HERE)
        generated_files = generate_modern_payslips(processed, month_name, year)

        return {
            "total_rows": len(df),
            "eligible_for_payslip": len(processed),
            "skipped_no_epf": skipped_no_epf,
            "missing_email": missing_email,
            "message": "Payslips generated successfully",
            "files": generated_files
        }


    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
    
@router.get("/download-all")
def download_all_payslips():
    folder_path = "generated_payslips"
    zip_path = f"{folder_path}/all_payslips.zip"

    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in os.listdir(folder_path):
            if file.endswith(".pdf"):
                zipf.write(
                    os.path.join(folder_path, file),
                    arcname=file
                )

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="All_Payslips.zip"
    )


