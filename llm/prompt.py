#prompt.py

job_selection_prompt = """
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

# Prompt for SMS message
sms_prompt_template = """
You are a notification writer.

Student name: {name}

Here are two jobs for the student:
1. {job1_title} at {job1_company} in {job1_location} ({job1_link})
2. {job2_title} at {job2_company} in {job2_location} ({job2_link})

Task:
Write a very short SMS (under 320 characters) to inform the student of these two jobs.
Return ONLY the text.
"""

# Prompt for Email message
email_prompt_template = """
You are an email copywriter.

Student name: {name}

Here are two jobs for the student:
1. {job1_title} at {job1_company} in {job1_location} ({job1_link})
2. {job2_title} at {job2_company} in {job2_location} ({job2_link})

Task:
Write a friendly but professional HTML email notifying the student of these jobs.

- Use <p> tags for paragraphs
- List the jobs inside <ul><li>…</li></ul>
- Make job titles bold using <b>…</b>
- Include clickable links with <a href="…">…</a>
- Return only the HTML body (no <html> or <body> tags)

<p>If you're interested in exploring these opportunities further, we encourage you to apply or reach out to us for more information.</p>
<p>Best regards,<br>
The JobAlert Team</p>

Do not invent any other signature or contact information.
Return only the HTML body content.
"""

