# scheduler.py

import time
import schedule
from main import send_job_alerts
from db.db import fetch_jobs

def job_alert_task():
    print("🚀 Running scheduled job alerts...")
    jobs = fetch_jobs()
    send_job_alerts(jobs)

if __name__ == "__main__":
    # Schedule the task to run once a day at 08:00 AM
    schedule.every().day.at("08:00").do(job_alert_task)

    print("⏳ Scheduler started... Running daily at 08:00 AM")
    while True:
        schedule.run_pending()
        time.sleep(60)  # check every minute
