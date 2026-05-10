import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils.web_search import search_web

# Loading environment variable
load_dotenv()

# API integration
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_research(topic, tone="Balanced", depth="Comprehensive"):
    """
    Generate a structured research report using:
    - Live web search results
    - User-selected tone
    - User-selected research depth
    """

    # Web search
    web_results = search_web(topic)

    # Promot building
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
    response = model.generate_content(prompt)
    return response.text