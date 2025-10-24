import sqlite3
from datetime import datetime

DB_NAME = "jobs.db"

# =========================
# 🧱 MAIN JOBS TABLE
# =========================
def init_jobs_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            link TEXT UNIQUE,
            keyword TEXT,
            scraped_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_jobs(jobs, keyword):
    """Save scraped jobs to database"""
    init_jobs_table()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for job in jobs:
        try:
            c.execute("""
                INSERT OR IGNORE INTO jobs (title, company, location, link, keyword, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                job['title'],
                job['company'],
                job['location'],
                job['link'],
                keyword,
                datetime.now()
            ))
        except Exception as e:
            print("⚠️ Error inserting job:", e)
    conn.commit()
    conn.close()


def fetch_jobs(keyword=None):
    """Fetch jobs from database"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if keyword:
        c.execute("SELECT title, company, location, link FROM jobs WHERE keyword=?", (keyword,))
    else:
        c.execute("SELECT title, company, location, link FROM jobs")
    rows = c.fetchall()
    conn.close()
    
    jobs = []
    for row in rows:
        jobs.append({
            "title": row[0],
            "company": row[1],
            "location": row[2],
            "link": row[3]
        })
    return jobs


# =========================
# 📬 SENT JOBS TABLE
# =========================
def init_sent_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create the sent_jobs table if not present
    c.execute("""
        CREATE TABLE IF NOT EXISTS sent_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email TEXT,
            job_link TEXT,
            channel TEXT,
            sent_at TIMESTAMP,
            UNIQUE(student_email, job_link, channel)
        )
    """)

    # Check existing columns (for migration)
    existing_cols = [col[1] for col in c.execute("PRAGMA table_info(sent_jobs)").fetchall()]

    # Add missing columns if necessary (no data loss)
    if "student_email" not in existing_cols:
        c.execute("ALTER TABLE sent_jobs ADD COLUMN student_email TEXT")
    if "channel" not in existing_cols:
        c.execute("ALTER TABLE sent_jobs ADD COLUMN channel TEXT")
    if "sent_at" not in existing_cols:
        c.execute("ALTER TABLE sent_jobs ADD COLUMN sent_at TIMESTAMP")

    conn.commit()
    conn.close()


def mark_job_sent(student_email, job_link, channel):
    """Mark a job as sent to a specific student on a specific channel"""
    init_sent_table()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO sent_jobs (student_email, job_link, channel, sent_at)
        VALUES (?, ?, ?, ?)
    """, (student_email, job_link, channel, datetime.now()))
    conn.commit()
    conn.close()


def job_already_sent(student_email, job_link, channel=None):
    """Check if a job has already been sent to a student (optionally by channel)"""
    init_sent_table()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if channel:
        c.execute("""
            SELECT 1 FROM sent_jobs 
            WHERE student_email=? AND job_link=? AND channel=? 
            LIMIT 1
        """, (student_email, job_link, channel))
    else:
        c.execute("""
            SELECT 1 FROM sent_jobs 
            WHERE student_email=? AND job_link=? 
            LIMIT 1
        """, (student_email, job_link))

    exists = c.fetchone() is not None
    conn.close()
    return exists


# =========================
# 🧩 SAFE MIGRATION RUNNER
# =========================
if __name__ == "__main__":
    init_jobs_table()
    init_sent_table()
    print("✅ Database upgraded successfully — no data lost!")
