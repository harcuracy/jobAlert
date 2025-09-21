# sms.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TERMI_API_KEY = os.getenv("TERMI_API_KEY")
TERMI_SENDER = 'jobAlert'

def send_sms(phone_number, job1, job2, student_name):
    """
    Sends SMS with 2 jobs to a student.
    job1 and job2 are dicts with 'title', 'company', 'location', 'link'.
    """
    message = f"Hi {student_name}, here are 2 jobs you may like:\n\n"
    message += f"1. {job1['title']} at {job1['company']}\n📍 {job1['location']}\nApply here: {job1['link']}\n\n"
    message += f"2. {job2['title']} at {job2['company']}\n📍 {job2['location']}\nApply here: {job2['link']}\n\n"
    message += "Reply STOP to unsubscribe."

    url = "https://api.ng.termii.com/api/sms/send"
    payload = {
        "to": phone_number,
        "from": TERMI_SENDER,
        "sms": message,
        "type": "plain",
        "channel": "generic",
        "api_key": TERMI_API_KEY,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"✅ SMS sent to {phone_number}")
    else:
        print(f"❌ Failed to send SMS to {phone_number}: {response.text}")
