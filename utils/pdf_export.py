from fpdf import FPDF
from utils.file_manager import sanitize_filename
def generate_pdf_data(topic, content):
    """
    Generate the PDF filename and bytes.
    """
    filename = sanitize_filename(topic) + ".pdf"

    #PDF creation
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    safe_content = content.encode("latin-1", "replace").decode("latin-1")
    pdf.write(8, safe_content)
    
    # pdf.output() returns the PDF bytearray in memory when no output file is provided
    pdf_bytes = bytes(pdf.output())

    return filename, pdf_bytes