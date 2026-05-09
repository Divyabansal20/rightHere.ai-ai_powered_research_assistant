import os


def sanitize_filename(topic):
    """
    Convert a topic into a safe filename.
    
    Example:
    'Artificial Intelligence in Healthcare'
    → 'artificial_intelligence_in_healthcare'
    """
    return topic.lower().replace(" ", "_")


def save_to_txt(topic, content):
    """
    Save the generated research content to a text file.
    
    Parameters:
    - topic: Research topic entered by the user
    - content: Generated research report
    """

    # Ensure output directory exists
    os.makedirs("research_outputs", exist_ok=True)

    # Create safe filename
    filename = sanitize_filename(topic) + ".txt"

    # Full path to output file
    filepath = os.path.join("research_outputs", filename)

    # Write content to file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

    # Return the saved file path
    return filepath