# rightHere.ai — AI Research Assistant

rightHere.ai is an AI research assistant that generates structured, well-formatted research reports on any topic. The application combines a modern Streamlit interface, live web search, and a large language model to deliver grounded research summaries with downloadable TXT and PDF exports.

The system is built as an AI agent using in-memory session states, enabling it to search the web in real-time, generate report summaries, and manage user-specific history and downloads without requiring persistent server disk storage. This makes the application **completely deployment-ready** and secure for multi-user cloud platforms.

---

## Features

* **Professional Web UI**: Clean, responsive Streamlit dashboard with a modern gradient theme.
* **Configurable Writing Tone**:
  * *Balanced*: Objective and comprehensive.
  * *Beginner*: Simple terms and easy-to-understand explanations.
  * *Technical*: Deep technical terminology and in-depth analyses.
  * *Business*: Strategic, high-level executive summaries.
* **Configurable Research Depth**: Supports *Basic*, *Detailed*, *Comprehensive*, and *Academic* depths.
* **Live Web Search**: Integrates DuckDuckGo text searches to retrieve the latest live web context.
* **Gemini LLM Integration**: Synthesizes and structures gathered research using Google Gemini (`gemini-2.5-flash`).
* **Privacy-Safe In-Memory Architecture**: History and generated reports are managed strictly in-memory per user session. There is **zero local filesystem persistence**, preventing history leaks between users in a multi-user deployment.
* **Instant Exports**: One-click download buttons to export reports as clean `.txt` or formatted `.pdf` files.
* **Robust Error Handling**: Gracefully handles API key exceptions, rate limiting (HTTP 429 quota limits), and empty inputs.

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
  In-Memory Session State
(Isolated TXT/PDF Generation)
            |
            v
  History and Downloads UI
```

---

## Component Integrations

### 1. Web Search
The assistant integrates a web search tool using DuckDuckGo (`ddgs`). Before generating a report, the agent retrieves relevant live snippets and feeds them to the language model as grounded context.
* **Implementation**: [utils/web_search.py](file:///c:/ai-intern-final-divya-bansal/utils/web_search.py)

### 2. In-Memory Document Generation
Rather than storing generated files on a local server directory (which is unsecure for multi-user settings and incompatible with ephemeral cloud instances), files are compiled as in-memory streams:
* **TXT generation**: Handled dynamically as a text stream.
* **PDF generation**: Handled in-memory using `fpdf2` by converting the document output to binary `bytes`.
* **Implementation**: [utils/file_manager.py](file:///c:/ai-intern-final-divya-bansal/utils/file_manager.py) and [utils/pdf_export.py](file:///c:/ai-intern-final-divya-bansal/utils/pdf_export.py)

---

## Project Structure

```text
ai-intern-final-divya-bansal/
│
├── app.py                   # Main Streamlit Application & Session Logic
├── requirements.txt         # Project Dependencies
├── README.md                # Documentation
├── .gitignore               # Ignored local configurations
├── .env                     # Local Environment Secrets (Ignored from Git)
│
├── utils/
│   ├── gemini_client.py     # Google Gemini API wrapper & prompt builder
│   ├── web_search.py        # DuckDuckGo search integration
│   ├── file_manager.py      # Filename sanitization & TXT generators
│   └── pdf_export.py        # In-memory FPDF2 export generator
│
└── screenshots/             # Interface and demo demonstration images
```

---

## Technology Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit |
| **Backend** | Python |
| **LLM API** | Google Gemini (`gemini-2.5-flash`) |
| **Web Search** | DuckDuckGo (`ddgs`) |
| **Storage & State** | Streamlit In-Memory Session State |
| **PDF Export** | `fpdf2` (bytes stream) |
| **Environment** | `python-dotenv` |

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

### 4. Configure Secrets
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> [!NOTE]
> You can acquire a free Gemini API key from [Google AI Studio](https://aistudio.google.com).

### 5. Run the Application
```bash
streamlit run app.py
```
The application will automatically launch at `http://localhost:8501`.

---

> 
> * **No Shared State**: When deployed, users will have completely isolated browser sessions—ensuring one user cannot view another user's research history or downloads.
> * **No Hard Disks Required**: The container filesystem can be completely read-only or ephemeral.
> * **API Keys**: Ensure you specify `GEMINI_API_KEY` under the deployment platform's **Secrets / Environment Variables** settings rather than committing your `.env` file.
