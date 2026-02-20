
import os
import calendar
import re
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image
)
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib import styles
from num2words import num2words
from reportlab.lib.styles import ParagraphStyle



#  COMPANY DETAILS
COMPANY_ADDRESS = "No.27, P.H. Road, Vanagaram, Chennai-600095."

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(BASE_DIR, "static", "logo.png")


def safe_filename(name):
    name = name.strip()
    name = re.sub(r'[\\/*?:"<>|]', "", name)  # remove illegal chars
    name = name.replace(" ", "_")             # replace spaces
    return name


def amount_in_words(amount):
    try:
        amount_int = int(float(amount))   # Only integer part
        words = num2words(amount_int, lang="en_IN").title()
        return words
    except:
        return "Zero"
    
def clean_money(value):
    try:
        return f"{float(value):.2f}"
    except:
        return "0.00"




def generate_modern_payslips(employees, month_name, year, pay_date):

    os.makedirs("generated_payslips", exist_ok=True)
    generated_files = []

    

    for emp in employees:

        employee_name_clean = safe_filename(emp["name"])
        file_name = f"{employee_name_clean}_payslip.pdf"

        file_path = os.path.join("generated_payslips", file_name)

        doc = SimpleDocTemplate(
            file_path,
            topMargin=15,   # reduce this
        )

        page_width = doc.width

        elements = []
        styles_sheet = styles.getSampleStyleSheet()

        # ================= LOGO =================
        if os.path.isfile(LOGO_PATH):
            logo = Image(LOGO_PATH)
            logo._restrictSize(4* inch, 2* inch)
            logo.hAlign = "LEFT"
            elements.append(logo)

        elements.append(Spacer(1, 2))

        # ================= ADDRESS =================
        address_style = styles_sheet["Normal"]
        address_style.leftIndent = 75   # adjust this value

        elements.append(Paragraph(COMPANY_ADDRESS, styles_sheet["Normal"]))
        elements.append(Spacer(1, 5))

        # ================= TITLE =================
        elements.append(
            Paragraph(
                f"<para align='center'><b>Payslip</b></para>",
                styles_sheet["Heading2"],
            )
        )
        elements.append(Spacer(1, 20))

        # ================= EMPLOYEE DETAILS =================
        details_data = [
            ["Employee Name:", emp["name"], "Paid Days:", emp["days_work"]],
            ["Pay Period:", f"{month_name} {year}", "LOP Days:", emp.get("lop_days", 0)],
            ["Pay Date:", pay_date, "OT Days:", emp.get("ot_days", 0)],
        ]

        details_table = Table(details_data, colWidths=[page_width/4]*4)
        details_table.hAlign = "LEFT"

        details_table.setStyle(
            TableStyle([
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),

                
                ("ALIGN", (0, 0), (1, -1), "LEFT"),
                ("ALIGN", (2, 0), (3, -1), "RIGHT"),
            ])
        )


        elements.append(details_table)
        elements.append(Spacer(1, 20))

        # ================= INCOME TABLE =================
        deductions = (
            emp["pf"] +
            emp["esi"] +
            emp["salary_adv"]
        )

        income_data = [
            ["Earnings", "Amount", "Deductions", "Amount"],
            ["Basic Salary", f"Rs {clean_money(emp['basic'])}",
            "Employee Provident Fund", f"Rs {clean_money(emp['pf'])}"],

            ["House Rent Allowance", f"Rs {clean_money(emp['hra'])}",
            "ESI", f"Rs {clean_money(emp['esi'])}"],

            ["Other Allowance", f"Rs {clean_money(emp.get('other_allowance', 0))}",
            "Advance", f"Rs {clean_money(emp.get('salary_adv', 0))}"],

            ["Gross Earnings", f"Rs {clean_money(emp['gross_wages'])}",
            "Total Deductions", f"Rs {clean_money(deductions)}"],
        ]


        income_table = Table(
            income_data,
            colWidths=[page_width*0.35, page_width*0.15,
                    page_width*0.35, page_width*0.15]
        )

        income_table.hAlign = "LEFT"


        income_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("LINEBEFORE", (2, 0), (2, -1), 1, colors.black),

                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),

                # Highlight totals
                ("BACKGROUND", (0, 4), (1, 4), colors.lightgrey),
                ("BACKGROUND", (2, 4), (3, 4), colors.lightgrey),
                ("FONTNAME", (0, 4), (3, 4), "Helvetica-Bold"),
            ])
        )

        elements.append(income_table)
        elements.append(Spacer(1, 25))

        # ================= NET PAY =================
        elements.append(
            Paragraph(
                f"<para align='center'><b>Net Pay: Rs {int(float(emp['net_pay']))}</b></para>",
                styles_sheet["Heading2"],
            )
        )

        elements.append(Spacer(1, 1))

        elements.append(
            Paragraph(
                f"<para align='center'>Amount In Words: {amount_in_words(emp['net_pay'])}</para>",
                styles_sheet["Normal"],
            )
        )

        elements.append(Spacer(1, 40))

        # ================= SIGNATURE =================
        signature_data = [["Employee Signature", "", "Authorized Signature"]]

        signature_table = Table(signature_data, colWidths=[page_width/3]*3)
        signature_table.hAlign = "LEFT"

        signature_table.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (2, 0), (2, 0), "RIGHT"),
            ])
        )

        elements.append(signature_table)

        # ===============================================
        footer_style = ParagraphStyle(
            "footer_style",
            parent=styles_sheet["Normal"],
            leftIndent=140,   # adjust this value
        )

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(
            Paragraph(
                "-This is system generated document-",
                footer_style
            )
        )



        doc.build(elements)
        generated_files.append(file_name)

    return generated_files
