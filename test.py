from notifications.sms import send_sms
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

        try:
            send_sms(student, job1, job2)
            print(f"✅ SMS successfully sent to {student['name']} ({student['phone']})")
            mark_job_sent(student["email"], job1, job2)
        except Exception as e:
            print(f"❌ SMS failed for {student['name']}: {e}")


# ✅ Add this part so the script actually runs
if __name__ == "__main__":
    print("🚀 Starting Job Alert Process...")
    jobs = fetch_jobs()  # Get available job list from database
    send_job_alerts(jobs)
    print("✅ Job alert process completed successfully!")
