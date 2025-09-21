# llm/formatter.py
import os
import json
import re
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq


from db import job_already_sent
from .prompt import job_selection_prompt
from .model import get_groq_llm




llm = get_groq_llm()



prompt = PromptTemplate(
    input_variables=["name", "department", "skills", "jobs_text"],
    template=job_selection_prompt
)

def parse_llm_json(raw_result):
    """Try to extract JSON from LLM output."""
    match = re.search(r"\{.*\}", raw_result, re.DOTALL)
    if match:
        json_text = match.group()
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            # Fix truncated JSON by closing braces
            json_text = json_text.rsplit("}", 1)[0] + "}"
            try:
                return json.loads(json_text)
            except:
                return None
    return None

def get_llm_job_selection(student, jobs, max_jobs=5):
    """Selects 2 relevant jobs using Groq LLM."""
    unsent_jobs = [job for job in jobs if not job_already_sent(job['link'])]

    if not unsent_jobs:
        return None

    # Limit jobs sent to LLM to avoid token limits
    jobs_text = "\n".join([
        f"{job['title']} at {job['company']} in {job['location']}, {job['link']}" 
        for job in unsent_jobs[:max_jobs]
    ])

    chain = LLMChain(llm=llm, prompt=prompt)
    raw_result = chain.run(
        name=student['name'],
        department=student['department'],
        skills=student.get('skills', 'N/A'),
        jobs_text=jobs_text
    )

    #print("===== LLM RAW OUTPUT =====")
    #print(raw_result)
    #print("==========================")

    selection = parse_llm_json(raw_result)
    return selection
