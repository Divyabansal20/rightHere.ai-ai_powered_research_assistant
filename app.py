from pathlib import Path
import streamlit as st
from utils.gemini_client import generate_research
from utils.file_manager import save_to_txt
from utils.pdf_export import save_to_pdf


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="rightHere.ai",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "history" not in st.session_state:
    output_dir = Path("research_outputs")
    output_dir.mkdir(exist_ok=True)

    history_items = []

    # Read all TXT files and reconstruct history
    for txt_file in sorted(
        output_dir.glob("*.txt"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    ):
        topic = txt_file.stem.replace("_", " ").title()

        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                report = f.read()
        except Exception:
            report = "Unable to load this report."

        pdf_file = txt_file.with_suffix(".pdf")

        history_items.append(
            {
                "topic": topic,
                "report": report,
                "txt_path": str(txt_file),
                "pdf_path": str(pdf_file) if pdf_file.exists() else "",
            }
        )

    st.session_state.history = history_items

if "downloads" not in st.session_state:
    output_dir = Path("research_outputs")
    output_dir.mkdir(exist_ok=True)

    # Load all existing TXT and PDF files from disk
    existing_files = sorted(
        [
            str(path)
            for path in output_dir.glob("*")
            if path.suffix.lower() in [".txt", ".pdf"]
        ],
        key=lambda p: Path(p).stat().st_mtime,
        reverse=True,
    )

    st.session_state.downloads = existing_files


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def clear_current_chat():
    """Clear only the currently displayed chat, preserving history."""
    for key in ["report", "topic", "txt_path", "pdf_path"]:
        if key in st.session_state:
            del st.session_state[key]


def add_to_history(topic, report, txt_path, pdf_path):
    """Add current research to history and downloads."""

    # Avoid duplicate history entries for the same topic in a row
    if (
        not st.session_state.history
        or st.session_state.history[-1]["topic"] != topic
    ):
        st.session_state.history.append(
            {
                "topic": topic,
                "report": report,
                "txt_path": txt_path,
                "pdf_path": pdf_path,
            }
        )

    # Track generated files
    for file_path in [txt_path, pdf_path]:
        if file_path not in st.session_state.downloads:
            st.session_state.downloads.append(file_path)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

* {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

/* Background */
.stApp {
    background: linear-gradient(160deg, #eef1ff 0%, #f5f0ff 35%, #e8f8ff 70%, #f0fdf4 100%) !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 900px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #eaecf4 !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.4rem 1.2rem 1rem 1.2rem !important;
}

.sidebar-logo-text {
    font-family: 'Sora', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
}

.gradient-text {
    background: linear-gradient(90deg, #3b5bdb, #06b6d4, #22c55e, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Sidebar section labels */
.sidebar-section-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9ba3b8;
    margin-top: 1.4rem;
    margin-bottom: 0.6rem;
}

/* Topbar */
.topbar {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    border: 1px solid #eaecf4;
    border-radius: 14px;
    padding: 0.65rem 1.4rem;
    margin-bottom: 2.2rem;
    font-family: 'Sora', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #1a1d2e;
}

/* Hero */
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: clamp(2rem, 4vw, 3.1rem);
    font-weight: 800;
    text-align: center;
    line-height: 1.2;
    color: #0f172a;
    letter-spacing: -0.03em;
    margin-bottom: 0.85rem;
}

.hero-subtitle {
    text-align: center;
    font-size: 1.02rem;
    color: #6b7280;
    line-height: 1.8;
    margin-bottom: 2.2rem;
}

/* Text area */
.stTextArea textarea {
    background: #ffffff !important;
    color: #111827 !important;
    border: 1.5px solid #e2e6f5 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(59,91,219,0.06) !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
    padding: 0.9rem 1.1rem !important;
}

.stTextArea textarea:focus {
    border: 1.5px solid #3b5bdb !important;
    box-shadow: 0 0 0 3px rgba(59,91,219,0.12) !important;
    outline: none !important;
}

/* Selectboxes */
.stSelectbox > div > div {
    background: #ffffff !important;
    border: 1.5px solid #e2e6f5 !important;
    border-radius: 12px !important;
    color: #374151 !important;
    min-height: 44px !important;
    box-shadow: 0 2px 6px rgba(59,91,219,0.05) !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #3b5bdb, #4f6bed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    width: 100% !important;
    height: 44px !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(59,91,219,0.25) !important;
}

section[data-testid="stSidebar"] .stButton {
    margin-bottom: 0.5px !important;   /* controls spacing between cards */
}

section[data-testid="stSidebar"] .stButton > button {
    background: rgba(59, 130, 246, 0.08) !important;
    color: #334155 !important;
    border: 1px solid rgba(59, 130, 246, 0.14) !important;
    border-radius: 12px !important;
    box-shadow: none !important;

    font-size: 0.90rem !important;
    font-weight: 500 !important;
    text-align: center !important;

    padding: 0.75rem 0.90rem !important;

    /* Remove button margin completely */
    margin: 0 !important;

    /* Reduce internal minimum height */
    min-height: 44px !important;

    /* Single-line text with ellipsis */
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;

    line-height: 1.2 !important;

    transition:
        background 0.2s ease,
        border-color 0.2s ease !important;
}

/* Hover effect */
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(59, 130, 246, 0.14) !important;
    border-color: rgba(59, 130, 246, 0.22) !important;
    color: #1e293b !important;
    transform: none !important;
}

/* Active/selected effect */
section[data-testid="stSidebar"] .stButton > button:focus,
section[data-testid="stSidebar"] .stButton > button:active {
    background: rgba(59, 130, 246, 0.18) !important;
    color: #0f172a !important;
    box-shadow: none !important;
    outline: none !important;
    transform: none !important;
}
/* Send button styling */

.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    width: 52px !important;
    height: 52px !important;
    min-width: 52px !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.30) !important;
    padding: 0 !important;
    margin-top: 22px !important;
    transition: all 0.25s ease !important;
}

/* Hover effect */
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #4f46e5) !important;
    color: #ffffff !important;
    box-shadow: 0 12px 30px rgba(59, 130, 246, 0.40) !important;
    transform: translateY(-2px) scale(1.03) !important;
}

/* Active click effect */
.stButton > button:active {
    transform: scale(0.96) !important;
}

/* Focus state */
.stButton > button:focus {
    outline: none !important;
    color: #ffffff !important;
}

/* Output card */
.output-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    border: 1px solid #eaecf4;
    box-shadow: 0 4px 20px rgba(15,23,42,0.05);
    margin-top: 1.4rem;
}

/* Force ALL output text to black */
.output-card,
.output-card *,
.output-card h1,
.output-card h2,
.output-card h3,
.output-card h4,
.output-card h5,
.output-card h6,
.output-card p,
.output-card li,
.output-card strong,
.output-card em,
.output-card span,
.output-card code,
.output-card pre,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] *,
.stSpinner span,
.stSpinner div {
    color: #111827 !important;
}

/* Download buttons */
.stDownloadButton > button {
    border-radius: 12px !important;
    border: 1px solid #dbe2f1 !important;
    background: #ffffff !important;
    color: #111827 !important;
    font-weight: 600 !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header {
    visibility: hidden;
}

[data-testid="stDecoration"] {
    display: none;
}
</style>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="sidebar-logo-text"><span class="gradient-text">rightHere.ai</span></div>',
        unsafe_allow_html=True,
    )

    if st.button("New Chat", use_container_width=True):
        clear_current_chat()
        st.rerun()

    # History
    st.markdown('<div class="sidebar-section-label">History</div>', unsafe_allow_html=True)

    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history)):
            topic_label = item["topic"].strip().replace("\n", " ")[:35]
            if st.button(
                topic_label,
                key=f"history_{idx}",
                use_container_width=True,
            ):
                st.session_state.report = item["report"]
                st.session_state.topic = item["topic"]
                st.session_state.txt_path = item["txt_path"]
                st.session_state.pdf_path = item["pdf_path"]
                st.rerun()
    else:
        st.caption("No research topics yet.")

    # Downloads
# ---------------- Downloads ----------------
    st.markdown(
        '<div class="sidebar-section-label">Downloads</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.downloads:
        for i, path in enumerate(reversed(st.session_state.downloads[-10:])):
            file_path = Path(path)

            # Skip if file does not exist
            if not file_path.exists():
                continue

            # Read file data
            with open(file_path, "rb") as f:
                file_data = f.read()

            # Sidebar download button
            st.download_button(
                label=f"{file_path.name}",
                data=file_data,
                file_name=file_path.name,
                mime=(
                    "application/pdf"
                    if file_path.suffix.lower() == ".pdf"
                    else "text/plain"
                ),
                use_container_width=True,
                key=f"sidebar_download_{i}",
            )
    else:
        st.caption("No generated files yet.")
# --------------------------------------------------
# Topbar
# --------------------------------------------------
st.markdown('<div class="topbar">AI Assistant</div>', unsafe_allow_html=True)


# --------------------------------------------------
# Hero Section
# --------------------------------------------------
st.markdown(
    """
<div class="hero-title">
    Know everything<br>
    in seconds <span class="gradient-text">rightHere...</span>
</div>
<div class="hero-subtitle">
    Your AI research assistant that finds, analyzes<br>
    and delivers the best insights instantly.
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Input Section
# --------------------------------------------------
st.markdown(
    """
    <div style="
        font-size: 0.95rem;
        font-weight: 600;
        color: #6b7280;
        margin-bottom: 0.6rem;
    ">
        What would you like to research?
    </div>
    """,
    unsafe_allow_html=True,
)

topic = st.text_area(
    label="Research Topic",
    placeholder="e.g. Impact of AI on renewable energy adoption...",
    height=120,
    label_visibility="collapsed",
    key="topic_input",
)

st.markdown("<div style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)

col1, col2, col_gap, col3 = st.columns([1.4, 1.4, 2.0, 0.38])

with col1:
    tone = st.selectbox(
        "Tone",
        ["Balanced", "Beginner", "Technical", "Business"],
        key="tone_select",
    )

with col2:
    depth = st.selectbox(
        "Research Depth",
        ["Comprehensive", "Basic", "Detailed", "Academic"],
        key="depth_select",
    )

with col3:
    generate_clicked = st.button("➤", key="send_btn")


# --------------------------------------------------
# Generate Research
# --------------------------------------------------
if generate_clicked:
    if not topic.strip():
        st.error("Please enter a research topic.")
    else:
        try:
            with st.spinner("Analyzing and synthesizing research..."):
                report = generate_research(
                    topic=topic,
                    tone=tone,
                    depth=depth,
                )

                txt_path = save_to_txt(topic, report)
                pdf_path = save_to_pdf(topic, report)

            # Save current result
            st.session_state.report = report
            st.session_state.topic = topic
            st.session_state.txt_path = txt_path
            st.session_state.pdf_path = pdf_path

            # Update history and downloads
            add_to_history(topic, report, txt_path, pdf_path)

            st.rerun()

        except Exception as e:
            st.error(f"An error occurred: {e}")
# --------------------------------------------------
# Display Research Result
# --------------------------------------------------
if "report" in st.session_state:
    st.markdown('<div class="output-card">', unsafe_allow_html=True)

    st.markdown("## Research Result")
    st.markdown(st.session_state.report)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Download TXT
    with col1:
        with open(st.session_state.txt_path, "rb") as f:
            st.download_button(
                label="⬇️ Download TXT",
                data=f.read(),
                file_name=Path(st.session_state.txt_path).name,
                mime="text/plain",
                use_container_width=True,
                key="download_txt",
            )

    # Download PDF
    with col2:
        with open(st.session_state.pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f.read(),
                file_name=Path(st.session_state.pdf_path).name,
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf",
            )

# --------------------------------------------------
# Optional Footer Spacing
# --------------------------------------------------
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)