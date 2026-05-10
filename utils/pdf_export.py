from fpdf import FPDF
from utils.file_manager import sanitize_filename
import os

def save_to_pdf(topic, content):
    """
    Save the generated research report as a PDF file.
    """
    # Creating output folder if it doesn't exist
    os.makedirs("research_outputs", exist_ok=True)

    filename = sanitize_filename(topic) + ".pdf"
    filepath = os.path.join("research_outputs", filename)

    #PDF creation
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    safe_content = content.encode("latin-1", "replace").decode("latin-1")
    pdf.write(8, safe_content)
    pdf.output(filepath)

    # Return saved path
    return filepath