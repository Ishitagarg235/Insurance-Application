# # my_pages/agent_studio.py

# import streamlit as st
# import threading
# import time
# from agents_core.crew_runner import run_insurance_crew


# # ── Page Styling ──────────────────────────────────────────────────────────────

# def _inject_styles():
#     st.markdown("""
#     <style>
#     /* Agent log card */
#     .log-card {
#         background: #1e1e2e;
#         border-left: 4px solid #7c3aed;
#         border-radius: 6px;
#         padding: 10px 14px;
#         margin-bottom: 8px;
#         font-family: monospace;
#         font-size: 0.85rem;
#         color: #e2e8f0;
#     }
#     .log-card .agent-name {
#         color: #a78bfa;
#         font-weight: bold;
#         font-size: 0.8rem;
#         text-transform: uppercase;
#         letter-spacing: 0.05em;
#     }
#     .log-card .event-name {
#         color: #34d399;
#         font-weight: 600;
#         margin-left: 8px;
#     }
#     .log-card .detail-text {
#         color: #94a3b8;
#         margin-top: 4px;
#         font-size: 0.78rem;
#         white-space: pre-wrap;
#     }

#     /* Researcher vs Writer color */
#     .researcher-card { border-left-color: #3b82f6; }
#     .researcher-card .agent-name { color: #60a5fa; }

#     .writer-card { border-left-color: #10b981; }
#     .writer-card .agent-name { color: #34d399; }

#     .system-card { border-left-color: #f59e0b; }
#     .system-card .agent-name { color: #fbbf24; }

#     /* Report output */
#     .report-box {
#         background: #0f172a;
#         border: 1px solid #334155;
#         border-radius: 10px;
#         padding: 24px;
#         margin-top: 16px;
#     }

#     /* Query examples */
#     .example-chip {
#         display: inline-block;
#         background: #1e293b;
#         border: 1px solid #475569;
#         border-radius: 20px;
#         padding: 4px 12px;
#         margin: 4px;
#         font-size: 0.8rem;
#         color: #94a3b8;
#         cursor: pointer;
#     }

#     /* Status badge */
#     .status-badge {
#         display: inline-block;
#         padding: 3px 10px;
#         border-radius: 12px;
#         font-size: 0.75rem;
#         font-weight: 600;
#     }
#     .status-running { background: #1e3a5f; color: #60a5fa; }
#     .status-done    { background: #064e3b; color: #34d399; }
#     .status-error   { background: #450a0a; color: #f87171; }
#     </style>
#     """, unsafe_allow_html=True)


# # ── Log Card Renderer ─────────────────────────────────────────────────────────

# def _render_log_card(log: dict):
#     agent = log.get("agent", "Agent")
#     event = log.get("event", "")
#     detail = log.get("detail", "")

#     # Pick card class by agent type
#     if "Researcher" in agent or "researcher" in agent.lower():
#         card_class = "log-card researcher-card"
#     elif "Writer" in agent or "writer" in agent.lower():
#         card_class = "log-card writer-card"
#     else:
#         card_class = "log-card system-card"

#     detail_html = f'<div class="detail-text">{detail[:250]}</div>' if detail else ""

#     st.markdown(f"""
#     <div class="{card_class}">
#         <span class="agent-name">{agent}</span>
#         <span class="event-name">{event}</span>
#         {detail_html}
#     </div>
#     """, unsafe_allow_html=True)


# # ── Session State Init ────────────────────────────────────────────────────────

# def _init_state():
#     defaults = {
#         "agent_running": False,
#         "agent_result": None,
#         "agent_logs": [],
#         "agent_query": "",
#         "agent_error": "",
#     }
#     for key, val in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = val


# # ── Background Runner ─────────────────────────────────────────────────────────

# def _run_crew_background(query: str):
#     """Runs crew in a thread so Streamlit doesn't block."""
#     result = run_insurance_crew(query)
#     st.session_state.agent_result = result
#     st.session_state.agent_logs = result.get("logs", [])
#     st.session_state.agent_running = False
#     st.session_state.agent_error = result.get("error", "")


# # ── Main Render ───────────────────────────────────────────────────────────────

# def render():
#     _inject_styles()
#     _init_state()

#     # ── Header ────────────────────────────────────────────────────────────────
#     st.markdown("## 🤖 Agent Studio")
#     st.markdown(
#         "Powered by **two collaborative AI agents** — "
#         "a Researcher that sources policy data and a Writer that formats it "
#         "into a clean report. Watch them work in real time."
#     )

#     # ── Agent Architecture Visual ─────────────────────────────────────────────
#     with st.expander("🏗️ How the agents work", expanded=False):
#         col1, col2, col3 = st.columns([2, 1, 2])
#         with col1:
#             st.markdown("""
#             **🔍 Researcher Agent**
#             - Searches the web for policy info
#             - Finds coverages, exclusions, premiums
#             - Outputs structured research notes
#             """)
#         with col2:
#             st.markdown("<br><br>**→ handoff →**", unsafe_allow_html=True)
#         with col3:
#             st.markdown("""
#             **✍️ Writer Agent**
#             - Receives Researcher's notes
#             - Rewrites in plain English
#             - Produces formatted report
#             """)

#     st.divider()

#     # ── Query Input ───────────────────────────────────────────────────────────
#     st.markdown("### 💬 What would you like to research?")

#     # Example query chips (buttons)
#     examples = [
#         "Term life insurance coverage",
#         "Health insurance exclusions",
#         "Car insurance third party vs comprehensive",
#         "Home insurance flood coverage",
#         "Travel insurance medical emergencies",
#     ]

#     st.markdown("**Quick examples:**")
#     cols = st.columns(len(examples))
#     for i, example in enumerate(examples):
#         with cols[i]:
#             if st.button(example, key=f"ex_{i}", use_container_width=True):
#                 st.session_state.agent_query = example

#     # Main text input
#     query = st.text_input(
#         label="Enter your insurance query",
#         value=st.session_state.agent_query,
#         placeholder="e.g. What does term life insurance cover?",
#         key="query_input",
#         label_visibility="collapsed",
#     )

#     # Run button
#     col_btn, col_status = st.columns([2, 5])
#     with col_btn:
#         run_clicked = st.button(
#             "🚀 Run Agents",
#             type="primary",
#             use_container_width=True,
#             disabled=st.session_state.agent_running,
#         )

#     with col_status:
#         if st.session_state.agent_running:
#             st.markdown(
#                 '<span class="status-badge status-running">⚡ Agents Running...</span>',
#                 unsafe_allow_html=True
#             )
#         elif st.session_state.agent_result:
#             if st.session_state.agent_result.get("success"):
#                 st.markdown(
#                     '<span class="status-badge status-done">✅ Complete</span>',
#                     unsafe_allow_html=True
#                 )
#             else:
#                 st.markdown(
#                     '<span class="status-badge status-error">❌ Error</span>',
#                     unsafe_allow_html=True
#                 )

#     # ── Trigger crew run ───────────

# my_pages/agent_studio.py

import streamlit as st
import time
from agents_core.crew_runner import run_insurance_crew, agent_logger

def _inject_styles():
    st.markdown("""
    <style>
    .log-card {
        background: #1e1e2e; border-left: 4px solid #7c3aed; border-radius: 6px;
        padding: 12px; margin-bottom: 10px; font-family: monospace; color: #e2e8f0;
    }
    .researcher-card { border-left-color: #3b82f6; }
    .writer-card { border-left-color: #10b981; }
    .system-card { border-left-color: #f59e0b; }
    .report-box {
        background: #0f172a; border: 1px solid #334155; border-radius: 10px;
        padding: 20px; margin: 15px 0;
    }
    .status-running { color: #60a5fa; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def render():
    _inject_styles()

    st.markdown("## 🤖 Agent Studio")
    st.caption("Two specialized agents working together (Researcher → Writer)")

    with st.expander("How it works", expanded=False):
        st.markdown("""
        **🔍 Researcher** → Searches web for policy details  
        **✍️ Writer** → Turns research into clean, customer-friendly report
        """)

    st.divider()

    # Query Input
    query = st.text_input(
        "What insurance topic do you want to research?",
        placeholder="e.g. What does term life insurance cover?",
        key="agent_query"
    )

    if st.button("🚀 Run Insurance Agents", type="primary", disabled=st.session_state.get("agent_running", False)):
        if not query.strip():
            st.warning("Please enter a query")
            st.stop()

        st.session_state.agent_running = True
        st.session_state.agent_logs = []
        st.session_state.agent_result = None
        st.rerun()

    # === Running State ===
    if st.session_state.get("agent_running"):
        with st.spinner("🤖 Agents are working... (this may take 20-60 seconds)"):
            result = run_insurance_crew(query.strip())
            
            st.session_state.agent_result = result
            st.session_state.agent_logs = result.get("logs", [])
            st.session_state.agent_running = False
            st.rerun()

    # === Show Logs ===
    if st.session_state.get("agent_logs"):
        st.markdown("### 📡 Agent Activity Log")
        for log in st.session_state.agent_logs:
            agent = log.get("agent", "")
            event = log.get("event", "")
            detail = log.get("detail", "")[:300]
            
            color = "🔵" if "Researcher" in agent else "🟢" if "Writer" in agent else "⚙️"
            st.markdown(f"""
            **{color} {agent}** — {event}  
            {detail}
            """)

    # === Show Final Result ===
    if st.session_state.get("agent_result"):
        result = st.session_state.agent_result
        if result.get("success"):
            st.success("✅ Report Generated Successfully!")
            
            with st.expander("🔍 Researcher's Raw Notes"):
                st.code(result.get("research_notes", ""), language="text")
            
            st.markdown("### 📄 Final Insurance Report")
            st.markdown(f'<div class="report-box">{result["final_report"]}</div>', unsafe_allow_html=True)

            st.download_button(
                "⬇️ Download Report as Markdown",
                data=result["final_report"],
                file_name=f"insurance_report_{query[:30]}.md",
                mime="text/markdown"
            )
        else:
            st.error(f"❌ Failed: {result.get('error')}")

    # Reset button
    if st.session_state.get("agent_result"):
        if st.button("🔄 New Query"):
            for key in ["agent_result", "agent_logs", "agent_running"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()