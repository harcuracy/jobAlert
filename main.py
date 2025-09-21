# pipeline


from llm.job_selector import get_llm_job_selection
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

        # --- Send WhatsApp ---
        try:
            send_whatsapp_message(student["phone"], student["name"], job1, job2)
            print(f"✅ WhatsApp message sent to {student['name']}")
        except Exception as e:
            print(f"❌ WhatsApp message failed for {student['name']}: {e}")

        # --- Send Email ---
        try:
            send_email(student, job1, job2)
        except Exception as e:
            print(f"❌ Email failed for {student['name']}: {e}")

        # --- Mark the jobs as sent ---
        mark_job_sent(job1['link'])
        mark_job_sent(job2['link'])

if __name__ == "__main__":
    jobs = fetch_jobs()  # fetch jobs from DB
    send_job_alerts(jobs)
