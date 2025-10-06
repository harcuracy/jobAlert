# pipeline.py

from llm.job_selector import get_llm_job_selection
from notifications.sms import send_sms
from notifications.email import send_email
from notifications.whatsapp import send_whatsapp_message
from db import mark_job_sent, fetch_jobs
from utils.helpers import read_students
from utils.constant import DATA_PATH


def send_job_alerts(jobs, csv_file=DATA_PATH):
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

        # --- 1️⃣ Send SMS ---
        try:
            send_sms(student, job1, job2)
            print(f"✅ SMS successfully sent to {student['name']} ({student['phone']})")
            #mark_job_sent(student["email"], job1, channel="sms")
            #mark_job_sent(student["email"], job2, channel="sms")
        except Exception as e:
            print(f"❌ SMS failed for {student['name']}: {e}")

        # --- 2️⃣ Send WhatsApp ---
        try:
            send_whatsapp_message(student["phone"], student["name"], job1, job2)
            print(f"✅ WhatsApp message sent to {student['name']}")
            #mark_job_sent(student["email"], job1, channel="whatsapp")
            #mark_job_sent(student["email"], job2, channel="whatsapp")
        except Exception as e:
            print(f"❌ WhatsApp message failed for {student['name']}: {e}")

        # --- 3️⃣ Send Email ---
        try:
            send_email(student, job1, job2)
            print(f"✅ Email successfully sent to {student['email']}")
            #mark_job_sent(student["email"], job1, channel="email")
            #mark_job_sent(student["email"], job2, channel="email")
        except Exception as e:
            print(f"❌ Email failed for {student['name']}: {e}")

    print("✅ Job alert process completed successfully!")


if __name__ == "__main__":
    print("🚀 Starting Job Alert Process...")
    jobs = fetch_jobs()  # fetch jobs from your database
    send_job_alerts(jobs)
