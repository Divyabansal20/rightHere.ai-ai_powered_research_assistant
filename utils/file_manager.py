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

def get_txt_data(topic, content):
    """
    Generate the text filename and return the contents.
    """
    filename = sanitize_filename(topic) + ".txt"
    return filename, content