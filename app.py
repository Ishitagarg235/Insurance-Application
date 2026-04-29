import streamlit as st
from styles import apply_carbon_theme

apply_carbon_theme()

# Shared session state
if "page" not in st.session_state:
    st.session_state.page = "home"

if "history" not in st.session_state:
    st.session_state.history = []

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hi! I'm your insurance expert. How can I help you today?"}
    ]

if "detail_item" not in st.session_state:
    st.session_state.detail_item = None

# Set page config
st.set_page_config(
    page_title="InsuranceAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("Multimodal Insurance AI")

nav_items = [
    ("🏠 Home", "home"),
    ("◈ Creator Studio", "studio"),
    ("◉ AI Expert Chat", "chat"),
    ("🤖 Agent Studio", "agent_studio"),  
    ("⊟ History", "history"),
    ("▦ Gallery", "gallery"),
]

for label, page_key in nav_items:
    is_active = st.session_state.page == page_key
    btn_type = "primary" if is_active else "secondary"
    if st.sidebar.button(label, use_container_width=True, type=btn_type, key=f"nav_{page_key}"):
        st.session_state.page = page_key
        st.rerun()

# Route to current page
try:
    page_module = __import__(f"my_pages.{st.session_state.page}", fromlist=[""])
    page_module.render()
except ImportError as e:
    st.error(f"Page not found: {st.session_state.page}. Error: {e}")