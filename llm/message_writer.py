from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from llm.model import get_groq_llm
from .prompt import sms_prompt_template, email_prompt_template

llm = get_groq_llm()

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

sms_chain = LLMChain(llm=llm, prompt=sms_prompt)
email_chain = LLMChain(llm=llm, prompt=email_prompt)

def generate_sms(student, job1, job2):
    return sms_chain.run(
        name=student['name'],
        job1_title=job1['title'], job1_company=job1['company'],
        job1_location=job1['location'], job1_link=job1['link'],
        job2_title=job2['title'], job2_company=job2['company'],
        job2_location=job2['location'], job2_link=job2['link']
    ).strip()

def generate_email(student, job1, job2):
    return email_chain.run(
        name=student['name'],
        job1_title=job1['title'], job1_company=job1['company'],
        job1_location=job1['location'], job1_link=job1['link'],
        job2_title=job2['title'], job2_company=job2['company'],
        job2_location=job2['location'], job2_link=job2['link']
    ).strip()
