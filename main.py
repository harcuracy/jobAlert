# Main function
from notifications.whatsapp import read_students,send_whatsapp_message
from llm.formatter import get_llm_job_selection
from db import mark_job_sent,fetch_jobs


# Main function
def send_job_alerts(jobs, csv_file="data/students.csv"):
    students = read_students(csv_file)

    for student in students:
        selection = get_llm_job_selection(student, jobs)
        if selection:
            job1 = selection.get("job1")
            job2 = selection.get("job2")
            if job1 and job2:
                send_whatsapp_message(student["phone"], student["name"], job1, job2)
                # Mark jobs as sent
                mark_job_sent(job1["link"])
                mark_job_sent(job2["link"])


if __name__ == "__main__":
    jobs = fetch_jobs()  # fetch all jobs
    send_job_alerts(jobs)
