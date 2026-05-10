# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
# from utils.web_search import search_web


# # Load variables from .env file
# load_dotenv()

# # Read API key from environment
# api_key = os.getenv("GEMINI_API_KEY")

# # Raise error if key is missing
# if not api_key:
#     raise ValueError("GEMINI_API_KEY not found in .env file")

# # Configure Gemini
# genai.configure(api_key=api_key)

# # Create model object
# model = genai.GenerativeModel("gemini-2.5-flash")


# def generate_research(topic):
#     """
#     Generate a structured research report using live web search results.
#     """

#     # Step 1: Search the web for the topic
#     web_results = search_web(topic)

#     # Step 2: Build a prompt containing both
#     # the user topic and the search results
#     prompt = f"""
#     You are an expert research assistant.

#     Research Topic:
#     {topic}

#     Web Search Results:
#     {web_results}

#     Using the web search results above, generate a detailed and well-structured research report.

#     Include the following sections:
#     1. Introduction
#     2. Key Concepts
#     3. Current Trends
#     4. Applications
#     5. Advantages
#     6. Challenges
#     7. Future Scope
#     8. Conclusion
#     9. References (include relevant URLs from the search results)

#     Write in a clear and professional format.
#     """

#     # Step 3: Send the prompt to Gemini
#     response = model.generate_content(prompt)

#     # Step 4: Return only the generated text
#     return response.text

import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils.web_search import search_web

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=api_key)

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_research(topic, tone="Balanced", depth="Comprehensive"):
    """
    Generate a structured research report using:
    - Live web search results
    - User-selected tone
    - User-selected research depth
    """

    # Step 1: Search the web
    web_results = search_web(topic)

    # Step 2: Build prompt
    prompt = f"""
You are an expert AI research assistant.

Research Topic:
{topic}

Writing Tone:
{tone}

Research Depth:
{depth}

Web Search Results:
{web_results}

Using the web search results above, generate a structured and well-formatted research report.

Requirements:
- Match the writing tone: {tone}
- Match the level of detail: {depth}
- Use professional formatting
- Include relevant references and URLs

Include the following sections:

1. Introduction
2. Key Concepts
3. Current Trends
4. Applications
5. Advantages
6. Challenges
7. Future Scope
8. Conclusion
9. References

Write in Markdown format using:
- Headings
- Bullet points
- Bold text where appropriate
"""

    # Step 3: Generate response
    response = model.generate_content(prompt)

    # Step 4: Return text
    return response.text