import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load variables from .env file
load_dotenv()

# Read API key from environment
api_key = os.getenv("GEMINI_API_KEY")

# Raise error if key is missing
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=api_key)

# Create model object
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_research(topic):
    """
    Generate a structured research report for the given topic.
    """

    prompt = f"""
    Generate a detailed research summary on the topic: {topic}

    Include the following sections:
    1. Introduction
    2. Key Concepts
    3. Applications
    4. Advantages
    5. Challenges
    6. Future Scope
    7. Conclusion

    Write in a clear and well-structured format.
    """

    response = model.generate_content(prompt)

    return response.text