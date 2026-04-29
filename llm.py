from groq import Groq
import streamlit as st


#load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

def _get_api_key() -> str:
    return st.secrets["GROQ_API_KEY"]

def _get_client() -> Groq:
    return Groq(api_key=_get_api_key())


def generate_text(prompt: str) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"Explain this insurance topic in very simple language:\n{prompt}",
            }
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content or ""
