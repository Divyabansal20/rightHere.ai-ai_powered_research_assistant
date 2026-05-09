from fpdf import FPDF
from utils.file_manager import sanitize_filename
import os


def save_to_pdf(topic, content):
    """
    Save the generated research report as a PDF file.
    """

    # Create output folder if it doesn't exist
    os.makedirs("research_outputs", exist_ok=True)

    # Generate safe filename
    filename = sanitize_filename(topic) + ".pdf"

    # Full file path
    filepath = os.path.join("research_outputs", filename)

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Convert unsupported Unicode characters to safe ASCII
    safe_content = content.encode("latin-1", "replace").decode("latin-1")

    # Write the entire content
    pdf.write(8, safe_content)

    # Save the PDF
    pdf.output(filepath)

    # Return saved path
    return filepath