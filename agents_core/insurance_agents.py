# agents_core/insurance_agents.py

import streamlit as st
from crewai import Agent, LLM


# ── LLM Setup (Fixed for Groq + CrewAI) ─────────────────────────────────────

def get_llm():
    """CrewAI LLM with Groq support"""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        st.error("❌ GROQ_API_KEY not found in .streamlit/secrets.toml")
        raise RuntimeError("Missing GROQ_API_KEY")

    return LLM(
        model="llama-3.3-70b-versatile",   # ← FIXED: no "groq/" prefix
        api_key=api_key,
        temperature=0.3,
        max_tokens=2048,
        base_url="https://api.groq.com/openai/v1",
    )

# ── Researcher Agent ──────────────────────────────────────────────────────────

def build_researcher(tools: list) -> Agent:
    return Agent(
        role="Insurance Policy Researcher",
        goal=(
            "Find accurate, detailed information about insurance policies, "
            "coverage terms, exclusions, and benefits."
        ),
        backstory=(
            "You are a seasoned insurance analyst with 15 years of experience "
            "researching various insurance policies."
        ),
        tools=tools,
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=10,
    )


# ── Writer Agent ──────────────────────────────────────────────────────────────

def build_writer() -> Agent:
    return Agent(
        role="Insurance Report Writer",
        goal=(
            "Transform raw research notes into clear, well-structured, "
            "customer-friendly insurance reports."
        ),
        backstory=(
            "You are an expert technical writer who makes complex insurance "
            "information easy to understand."
        ),
        tools=[],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
    )