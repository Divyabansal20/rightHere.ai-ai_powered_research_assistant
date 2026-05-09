from utils.gemini_client import generate_research
from utils.file_manager import save_to_txt
from utils.pdf_export import save_to_pdf

topic = "Artificial Intelligence in Healthcare"

# Generate research report
result = generate_research(topic)

# Save as TXT
txt_path = save_to_txt(topic, result)

# Save as PDF
pdf_path = save_to_pdf(topic, result)

# Print report
print(result)

# Show file locations
print(f"\nTXT saved to: {txt_path}")
print(f"PDF saved to: {pdf_path}")