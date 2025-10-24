# llm/model.py
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_groq_llm(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    max_retries=2,
    timeout=None,
    api_key=None
):
    """Return a preconfigured Groq LLM instance."""
    if api_key is None:
        api_key = os.getenv("GROQ_API_KEY")

    return ChatGroq(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        max_retries=max_retries,
        api_key=api_key
    )
