from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm.model import get_groq_llm
from .prompt import sms_prompt_template, email_prompt_template

# Initialize LLM
llm = get_groq_llm()

# Define prompt templates
sms_prompt = PromptTemplate(
    input_variables=[
        "name",
        "job1_title","job1_company","job1_location","job1_link",
        "job2_title","job2_company","job2_location","job2_link"
    ],
    template=sms_prompt_template
)

email_prompt = PromptTemplate(
    input_variables=[
        "name",
        "job1_title","job1_company","job1_location","job1_link",
        "job2_title","job2_company","job2_location","job2_link"
    ],
    template=email_prompt_template
)

# Define parsers
parser = StrOutputParser()

# Build chains using LCEL
sms_chain = sms_prompt | llm | parser
email_chain = email_prompt | llm | parser

# Generator functions
def generate_sms(student, job1, job2):
    return sms_chain.invoke({
        "name": student["name"],
        "job1_title": job1["title"], "job1_company": job1["company"],
        "job1_location": job1["location"], "job1_link": job1["link"],
        "job2_title": job2["title"], "job2_company": job2["company"],
        "job2_location": job2["location"], "job2_link": job2["link"]
    }).strip()

def generate_email(student, job1, job2):
    return email_chain.invoke({
        "name": student["name"],
        "job1_title": job1["title"], "job1_company": job1["company"],
        "job1_location": job1["location"], "job1_link": job1["link"],
        "job2_title": job2["title"], "job2_company": job2["company"],
        "job2_location": job2["location"], "job2_link": job2["link"]
    }).strip()
