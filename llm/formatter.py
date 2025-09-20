# llm/formatter.py
import os
import json
import re
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from db import job_already_sent

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    api_key=GROQ_API_KEY
)

# Prompt template: only pick 2 jobs and return JSON
prompt_template = """
You are a job recommendation engine.

Student name: {name}
Department: {department}
Skills: {skills}

Available jobs:
{jobs_text}

Task:
Select the **2 most relevant jobs** for this student.
Return ONLY a JSON object in this format:

{{
  "job1": {{"title": "", "company": "", "location": "", "link": ""}},
  "job2": {{"title": "", "company": "", "location": "", "link": ""}}
}}
"""

prompt = PromptTemplate(
    input_variables=["name", "department", "skills", "jobs_text"],
    template=prompt_template
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
