import os
import re


# Generating a filename
def sanitize_filename(topic):
    """
    Convert a research topic into a safe filename.
    Example:
    "Artificial Intelligence in Healthcare"
    -> "artificial_intelligence_in_healthcare"
    """

    # Preprocessing on topic name 
    topic = topic.strip()
    topic = re.sub(r"\s+", "_", topic)
    topic = re.sub(r'[\\/:*?"<>|]', "", topic)
    topic = topic.lower()
    topic = topic[:80]

    # If topic becomes empty
    if not topic:
        topic = "research_report"
    return topic

# Adding file content 

def save_to_txt(topic, content):
    """
    Save generated research content to a text file.
    """
    os.makedirs("research_outputs", exist_ok=True)

    filename = sanitize_filename(topic) + ".txt"
    filepath = os.path.join("research_outputs", filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

    return filepath