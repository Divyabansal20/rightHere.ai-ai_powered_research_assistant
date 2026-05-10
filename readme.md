# rightHere.ai — AI Research Assistant

rightHere.ai is an AI research assistant that generates structured, well-formatted research reports on any topic. The application combines a modern Streamlit interface, live web search, and a large language model to deliver grounded research summaries with downloadable TXT and PDF exports.

The system is designed as an AI agent with multiple MCP-style tools, enabling it to retrieve external information and persist generated outputs.

---
## Features

* Accepts any research topic through a professional web interface
* Supports configurable writing tone:

  * Balanced
  * Beginner
  * Technical
  * Business
* Supports configurable research depth:

  * Basic
  * Detailed
  * Comprehensive
  * Academic
* Performs live web search to gather current information
* Generates structured research reports using Google Gemini
* Saves each report as both TXT and PDF
* Maintains persistent History and Downloads across application restarts
* Provides one-click downloads from the UI
* Handles empty inputs, API quota limits, and runtime errors gracefully

---

## Architecture Overview

```text
        User Input 
            |
            v
      Web Search MCP
       (DuckDuckGo)
            |
            v
        Gemini API
            |
            v
  Structured Research Report
            |
            v
     File System MCP
   (TXT/PDF Persistence)
            |
            v
  History and Downloads UI
```

---

## MCP Integrations

### 1. Web Search MCP

The assistant integrates a web search tool using DuckDuckGo (`ddgs`). Before generating a report, the agent retrieves current search results and uses them as context for the language model.

**Implementation:** 
* `utils/web_search.py`

---

### 2. File System MCP

The assistant saves every generated report to the local `research_outputs/` directory in both TXT and PDF formats. On application startup, the system scans this directory to rebuild the History and Downloads panels.

**Implementation:**

* `utils/file_manager.py`
* `utils/pdf_export.py`

---

## LLM Integration

The application uses Google Gemini (`gemini-2.5-flash`) to generate research reports.

The LLM receives:
* The user's research topic
* Selected tone and depth preferences
* Live web search results

The model returns a structured report containing:
* Introduction
* Key Concepts
* Current Trends
* Applications
* Advantages
* Challenges
* Future Scope
* Conclusion
* References

---

## Project Structure

```text
ai-intern-final-divya-bansal/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── utils/
│   ├── gemini_client.py
│   ├── web_search.py
│   ├── file_manager.py
│   └── pdf_export.py
│
├── research_outputs/        # Auto-generated at runtime
└── screenshots/             # Optional demonstration images
```

---

## Technology Stack

| Component              | Technology          |
| ---------------------- | ------------------- |
| Frontend               | Streamlit           |
| Backend                | Python              |
| LLM API                | Google Gemini       |
| Web Search MCP         | DuckDuckGo (`ddgs`) |
| File System MCP        | Local filesystem    |
| PDF Export             | `fpdf2`             |
| Environment Management | `python-dotenv`     |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Divyabansal20/ai-intern-final-divya-bansal.git
cd ai-intern-final-divya-bansal
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

### 5. Get a Gemini API Key

Generate a free API key from Google AI Studio:

[https://aistudio.google.com](https://aistudio.google.com)

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Error Handling

The application includes robust error handling for:
* Empty research topics
* Missing API keys
* API quota limits (HTTP 429)
* Network errors
* File generation failures

---

## Deployment Considerations

The current implementation uses a local file-based persistence layer. This is ideal for demonstrating MCP-based file interactions and works well for single-user use cases.

For multi-user production deployments, the File System MCP can be replaced with cloud storage and a database (e.g., Firebase, Supabase, or AWS S3) to isolate user data and provide durable storage.
