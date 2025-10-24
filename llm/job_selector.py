# llm/formatter.py
import os
import json
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from db.db import job_already_sent
from .prompt import job_selection_prompt
from .model import get_groq_llm


# Initialize Groq LLM
llm = get_groq_llm()

# Define prompt template
prompt = PromptTemplate(
    input_variables=["name", "department", "skills", "jobs_text"],
    template=job_selection_prompt
)

# Parser to extract only string output from LLM
parser = StrOutputParser()

# Build the LCEL chain (replaces deprecated LLMChain)
chain = prompt | llm | parser


def parse_llm_json(raw_result):
    """Try to extract JSON from LLM output."""
    match = re.search(r"\{.*\}", raw_result, re.DOTALL)
    if match:
        json_text = match.group()
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            # Try to fix truncated JSON
            json_text = json_text.rsplit("}", 1)[0] + "}"
            try:
                return json.loads(json_text)
            except Exception:
                return None
    return None


def get_llm_job_selection(student, jobs, max_jobs=5):
    """Selects relevant jobs using Groq LLM."""
    # Only include jobs that have not already been sent to this student
    unsent_jobs = [
        job for job in jobs
        if not job_already_sent(student["email"], job["link"])
    ]

    if not unsent_jobs:
        return None

    # Limit jobs sent to LLM to avoid token overflow
    jobs_text = "\n".join([
        f"{job['title']} at {job['company']} in {job['location']}, {job['link']}"
        for job in unsent_jobs[:max_jobs]
    ])

    # Run the modern LCEL chain
    raw_result = chain.invoke({
        "name": student["name"],
        "department": student["department"],
        "skills": student.get("skills", "N/A"),
        "jobs_text": jobs_text
    })

    selection = parse_llm_json(raw_result)
    return selection
