import os
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd
import calendar
from datetime import datetime
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
    
    match = re.search(r'([A-Za-z]{3})\s*(\d{2})', filename)

    if match:
        month_short = match.group(1).title()   
        year_short = int(match.group(2))       
        
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


def extract_month_date_from_sheet(raw_df):
    month_name = None
    year = None
    pay_date = None

    for _, row in raw_df.iterrows():
        for i, cell in enumerate(row):
            if pd.isna(cell):
                continue

            # 🔹 Detect MONTH row
            if isinstance(cell, str) and cell.strip().lower() == "month":

                next_cell = row[i + 1]

                # Case 1: If it's already datetime
                if isinstance(next_cell, datetime):
                    month_name = calendar.month_name[next_cell.month]
                    year = next_cell.year

                # Case 2: If it's string like "Jan-26"
                elif isinstance(next_cell, str):
                    value = next_cell.strip()

                    match = re.search(r'([A-Za-z]{3})[-/ ]?(\d{2,4})', value)

                    if match:
                        month_abbr = match.group(1).title()
                        year_part = match.group(2)

                        # Convert 26 → 2026
                        if len(year_part) == 2:
                            year = 2000 + int(year_part)
                        else:
                            year = int(year_part)

                        try:
                            month_number = datetime.strptime(month_abbr, "%b").month
                            month_name = calendar.month_name[month_number]
                        except:
                            month_name = month_abbr

            # 🔹 Detect DATE row
            if isinstance(cell, str) and cell.strip().lower() == "date":
                next_cell = row[i + 1]

                if isinstance(next_cell, datetime):
                    pay_date = next_cell.strftime("%d-%m-%Y")

                elif isinstance(next_cell, str):
                    pay_date = next_cell.strip()

    return month_name, year, pay_date

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
        raw_df = pd.read_excel(file_path, header=None)

        month_name, year, pay_date = extract_month_date_from_sheet(raw_df)

        # STEP 3 — Read Excel
        raw_df = pd.read_excel(file_path, header=None)
        df = pd.read_excel(file_path, header=3)

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
                "lop_days": safe_float(row.get("lop_days"))
                
            })

        # STEP 5 — Generate Payslips (ONLY HERE)
        generated_files = generate_modern_payslips(processed,month_name,year,pay_date)

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

@router.get("/preview/{filename}")
def preview_payslip(filename: str):
    file_path = os.path.join("generated_payslips", filename)

    return FileResponse(
        file_path,
        media_type="application/pdf"
    )
    
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


