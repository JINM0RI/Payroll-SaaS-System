import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


def generate_modern_payslips(processed_employees, month="Jan 2026"):

    os.makedirs("generated_payslips", exist_ok=True)
    styles = getSampleStyleSheet()
    generated_files = []

    for emp in processed_employees:

        filename = f"payslip_{emp['emp_id']}.pdf"
        filepath = os.path.join("generated_payslips", filename)

        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []

        # ===== COMPANY HEADER =====
        elements.append(Paragraph("<b>SACISTHA GRANITE</b>", styles["Title"]))
        elements.append(Spacer(1, 0.15 * inch))
        elements.append(Paragraph(f"Salary Slip for {month}", styles["Heading3"]))
        elements.append(Spacer(1, 0.3 * inch))

        # ===== EMPLOYEE DETAILS SECTION =====
        details = [
            ["Employee ID", emp["emp_id"]],
            ["Employee Name", emp["name"]],
            ["Days Worked", emp["days_work"]],
        ]

        details_table = Table(details, colWidths=[2.5 * inch, 3 * inch])
        details_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ]))

        elements.append(details_table)
        elements.append(Spacer(1, 0.4 * inch))

        # ===== EARNINGS TABLE =====
        earnings = [
            ["EARNINGS", "AMOUNT"],
            ["Basic + DA", f"{emp['basic']:.2f}"],
            ["HRA", f"{emp['hra']:.2f}"],
            ["OT Amount", f"{emp['ot_amount']:.2f}"],
            ["Gross Wages", f"{emp['gross_wages']:.2f}"],
            ["Earned Wages", f"{emp['earned_wages']:.2f}"],
        ]

        earnings_table = Table(earnings, colWidths=[3 * inch, 2 * inch])
        earnings_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ]))

        elements.append(earnings_table)
        elements.append(Spacer(1, 0.4 * inch))

        # ===== DEDUCTIONS TABLE =====
        deductions = [
            ["DEDUCTIONS", "AMOUNT"],
            ["EPF (12%)", f"{emp['pf']:.2f}"],
            ["ESI (0.75%)", f"{emp['esi']:.2f}"],
            ["Salary Advance", f"{emp['salary_adv']:.2f}"],
        ]

        deductions_table = Table(deductions, colWidths=[3 * inch, 2 * inch])
        deductions_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ]))

        elements.append(deductions_table)
        elements.append(Spacer(1, 0.5 * inch))

        # ===== NET PAY HIGHLIGHT =====
        net = [
            ["NET PAY", f"{emp['net_pay']:.2f}"]
        ]

        net_table = Table(net, colWidths=[3 * inch, 2 * inch])
        net_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.lightgreen),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ]))

        elements.append(net_table)

        doc.build(elements)
        generated_files.append(filepath)

    return generated_files
