import tempfile

from fpdf import FPDF



# def save_report_to_pdf(report_text, filename):
#     report_text = str(report_text)
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     for line in report_text.split('\n'):
#         pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('utf-8'))
#         print(line)


#     tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
#     pdf.output(tmp_file.name)
#     return tmp_file.name


from fpdf import FPDF
import tempfile

def save_report_to_pdf(report_text, filename="diagnostic_report.pdf"):
    report_text = str(report_text)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()


    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "MEDICAL DIAGNOSTIC REPORT", ln=True, align='C')
    pdf.ln(10)


    pdf.set_font("Arial", size=12)

    for line in report_text.split('\n'):
        clean_line = line.strip()

        
       
        if clean_line == "--------------------":
            pdf.ln(3)
            pdf.set_draw_color(150, 150, 150)  # Light gray line
            pdf.set_line_width(0.4)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)

        elif clean_line == "":
            pdf.ln(5)

        elif clean_line.startswith("Patient Information:") or \
             clean_line.startswith("Diagnosis Summary:") or \
             clean_line.startswith("Tumor Characteristics:") or \
             clean_line.startswith("Clinical Interpretation:") or \
             clean_line.startswith("Suggested Next Steps:") or \
             clean_line.startswith("Notes:"):

            pdf.ln(5)
            pdf.set_font("Arial", 'B', 13)
            pdf.cell(0, 10, clean_line, ln=True)
            pdf.set_font("Arial", size=12)
            pdf.ln(2)
        else:
            pdf.multi_cell(0, 10, clean_line.encode('latin-1', 'replace').decode('latin-1'))

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)
    return tmp_file.name

