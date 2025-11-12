#main.py

from llm.job_selector import get_llm_job_selection
from notifications.sms import send_sms
from notifications.email import send_email
from notifications.whatsapp import send_whatsapp_message
from db.db import mark_job_sent, fetch_jobs, job_already_sent
from utils.helpers import read_students
from utils.constant import DATA_PATH


def send_job_alerts(jobs, csv_file=DATA_PATH):
    """Send job alerts to students via SMS, WhatsApp, and Email (no duplicates)."""
    students = read_students(csv_file)

    for student in students:
        print(f"\n👤 Processing alerts for: {student['name']} ({student['email']})")

        # Get personalized job selection for the student
        selection = get_llm_job_selection(student, jobs)
        if not selection:
            print(f"⚠️ No valid job selection for {student['name']}")
            continue

        job1 = selection.get("job1")
        job2 = selection.get("job2")

        if not job1 or not job2:
            print(f"⚠️ Incomplete job data for {student['name']}")
            continue

        # Define communication channels and their corresponding send functions
        channels = {
            "sms": send_sms,
            "whatsapp": send_whatsapp_message,
            "email": send_email
        }

        for channel, send_func in channels.items():
            # Check if BOTH jobs have already been sent on this channel
            already_sent_1 = job_already_sent(student["email"], job1["link"], channel)
            already_sent_2 = job_already_sent(student["email"], job2["link"], channel)

            if already_sent_1 and already_sent_2:
                print(f"⏩ Skipping {channel.upper()} for {student['name']} — already sent both jobs.")
                continue

            try:
                # Send messages for this channel
                if channel == "sms":
                    send_func(student, job1, job2)
                elif channel == "whatsapp":
                    send_func(student["phone"], student["name"], job1, job2)
                else:  # email
                    send_func(student, job1, job2)

                # Mark jobs as sent
                mark_job_sent(student["email"], job1["link"], channel)
                mark_job_sent(student["email"], job2["link"], channel)

                print(f"✅ {channel.upper()} alert sent successfully to {student['name']}")

            except Exception as e:
                print(f"❌ Failed to send via {channel.upper()} for {student['name']}: {e}")

    print("\n🎯 All job alerts processed successfully!")


if __name__ == "__main__":
    print("🚀 Starting Job Alert Process...")
    jobs = fetch_jobs()  # fetch jobs from database
    send_job_alerts(jobs)
