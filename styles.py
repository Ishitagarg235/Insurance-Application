# # styles.py
import streamlit as st

def apply_carbon_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono&display=swap');

        :root {
            --ibm-blue: #0f62fe;
            --ibm-gray-10: #f4f4f4;
            --ibm-gray-90: #161616;
            --ibm-text: #161616;
            --ibm-text-secondary: #525252;
        }

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'IBM Plex Sans', sans-serif;
            background: var(--ibm-gray-10);
        }

        /* ── Fix: all main content text must be dark ── */
        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] label,
        [data-testid="stAppViewContainer"] li,
        [data-testid="stAppViewContainer"] td,
        [data-testid="stAppViewContainer"] th {
            color: var(--ibm-text) !important;
        }

        /* ── Dropdown: selected value text must be light (dark box bg) ── */
        [data-testid="stSelectbox"] div[data-baseweb="select"] span,
        [data-testid="stSelectbox"] div[data-baseweb="select"] div,
        [data-testid="stSelectbox"] [role="combobox"] *,
        [data-testid="stSelectbox"] input {
            color: #f4f4f4 !important;
        }

        /* ── Dropdown open: option list items ── */
        [data-testid="stSelectbox"] ul li,
        [role="listbox"] li,
        [role="option"] {
            color: #f4f4f4 !important;
            background-color: #2b2b2b !important;
        }
        [role="option"]:hover,
        [role="option"][aria-selected="true"] {
            background-color: #0f62fe !important;
            color: #ffffff !important;
        }

        /* ── Headers ── */
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] h4,
        [data-testid="stAppViewContainer"] h5,
        [data-testid="stAppViewContainer"] h6 {
            color: var(--ibm-text) !important;
        }

        /* ── st.header / st.subheader ── */
        [data-testid="stHeading"] {
            color: var(--ibm-text) !important;
        }

        /* ── st.caption ── */
        [data-testid="stCaptionContainer"] p,
        .stCaption p {
            color: var(--ibm-text-secondary) !important;
        }

        /* ── st.markdown plain text ── */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span {
            color: var(--ibm-text) !important;
        }

        /* ── st.write / st.text ── */
        [data-testid="stText"] {
            color: var(--ibm-text) !important;
        }

        /* ── selectbox & text_area labels ── */
        [data-testid="stSelectbox"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stTextInput"] label {
            color: var(--ibm-text) !important;
            font-weight: 500 !important;
        }

        /* ── Expander title ── */
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span {
            color: var(--ibm-text) !important;
            font-weight: 500 !important;
        }

        /* ── Tab labels ── */
        [data-testid="stTabs"] button p,
        [data-testid="stTabs"] button span {
            color: var(--ibm-text) !important;
        }

        /* ── Chat messages ── */
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] span {
            color: var(--ibm-text) !important;
        }

        /* ── Sidebar: keep white text only there ── */
        .stSidebar,
        .stSidebar p,
        .stSidebar span,
        .stSidebar div,
        .stSidebar label {
            color: #ffffff !important;
        }

        .stSidebar {
            background: var(--ibm-gray-90) !important;
        }

        /* ── Sidebar title ── */
        .stSidebar > div > div > div > h1,
        .stSidebar > div > div > div > h2,
        .stSidebar > div > div > div > h3 {
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.6rem !important;
            letter-spacing: 0.8px !important;
            margin: 1rem 0 1.5rem 0 !important;
            padding-bottom: 0.6rem !important;
            border-bottom: 1px solid rgba(0, 240, 255, 0.25) !important;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.7) !important;
        }

        /* ── Nav buttons ── */
        .nav-button {
            width: 100% !important;
            margin: 6px 0 !important;
            text-align: left !important;
            font-weight: 500 !important;
        }

        .nav-active {
            background: var(--ibm-blue) !important;
            color: white !important;
        }

        /* ── Section titles ── */
        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin: 1.5rem 0 0.8rem;
            color: var(--ibm-text) !important;
        }

    </style>
    """, unsafe_allow_html=True)