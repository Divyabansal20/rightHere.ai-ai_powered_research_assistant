# import os


# def sanitize_filename(topic):
#     """
#     Convert a topic into a safe filename.
    
#     Example:
#     'Artificial Intelligence in Healthcare'
#     → 'artificial_intelligence_in_healthcare'
#     """
#     return topic.lower().replace(" ", "_")


# def save_to_txt(topic, content):
#     """
#     Save the generated research content to a text file.
    
#     Parameters:
#     - topic: Research topic entered by the user
#     - content: Generated research report
#     """

#     # Ensure output directory exists
#     os.makedirs("research_outputs", exist_ok=True)

#     # Create safe filename
#     filename = sanitize_filename(topic) + ".txt"

#     # Full path to output file
#     filepath = os.path.join("research_outputs", filename)

#     # Write content to file
#     with open(filepath, "w", encoding="utf-8") as file:
#         file.write(content)

#     # Return the saved file path
#     return filepath

import os
import re


def sanitize_filename(topic):
    """
    Convert a research topic into a safe filename.

    Example:
    "Artificial Intelligence in Healthcare"
    -> "artificial_intelligence_in_healthcare"
    """

    # Remove leading/trailing whitespace and newlines
    topic = topic.strip()

    # Replace all whitespace (spaces, tabs, newlines) with underscores
    topic = re.sub(r"\s+", "_", topic)

    # Remove characters not allowed in filenames
    topic = re.sub(r'[\\/:*?"<>|]', "", topic)

    # Convert to lowercase
    topic = topic.lower()

    # Limit filename length
    topic = topic[:80]

    # Fallback if topic becomes empty
    if not topic:
        topic = "research_report"

    return topic


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