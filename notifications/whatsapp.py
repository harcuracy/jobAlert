# notifications/whatsapp.py
import os
import csv
import requests
from db import mark_job_sent, job_already_sent, fetch_jobs
from llm.formatter import get_llm_job_selection

from dotenv import load_dotenv
load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")


def send_whatsapp_message(phone_number, student_name, job1, job2):
    """
    Sends the approved WhatsApp template 'job_alert_notification_2jobs' with 2 jobs.
    job1 and job2 are dicts with 'title', 'company', 'location', 'link'.
    """
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "job_alert_notification_2jobs",
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": student_name},
                        {"type": "text", "text": job1['title']},
                        {"type": "text", "text": job1['company']},
                        {"type": "text", "text": job1['location']},
                        {"type": "text", "text": job1['link']},
                        {"type": "text", "text": job2['title']},
                        {"type": "text", "text": job2['company']},
                        {"type": "text", "text": job2['location']},
                        {"type": "text", "text": job2['link']}
                    ]
                }
            ]
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"✅ Sent template to {phone_number}")
    else:
        print(f"❌ Failed for {phone_number}: {response.text}")


def read_students(csv_file="data/students.csv"):
    students = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({
                "name": row["name"],
                "phone": row["phone"],
                "department": row["department"],
                "skills": row.get("skills", "")
            })
    return students


def send_job_alerts(jobs, csv_file="data/students.csv"):
    students = read_students(csv_file)

    for student in students:
        selection = get_llm_job_selection(student, jobs)
        if not selection:
            print(f"⚠️ No valid job selection for {student['name']}")
            continue

        job1 = selection.get("job1")
        job2 = selection.get("job2")

        if not job1 or not job2:
            print(f"⚠️ Incomplete job data for {student['name']}")
            continue

        send_whatsapp_message(student["phone"], student["name"], job1, job2)

        # Mark jobs as sent
        mark_job_sent(job1['link'])
        mark_job_sent(job2['link'])


if __name__ == "__main__":
    jobs = fetch_jobs()
    send_job_alerts(jobs)
