from utils.gemini_client import generate_research
from utils.file_manager import save_to_txt

topic = "Artificial Intelligence in Healthcare"

# Generate research report
result = generate_research(topic)

# Save to text file
saved_path = save_to_txt(topic, result)

# Print report
print(result)

# Show where the file was saved
print(f"\nReport saved to: {saved_path}")