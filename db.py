# db.py
import sqlite3
from datetime import datetime

DB_NAME = "jobs.db"

# Initialize main jobs table
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

# Save jobs to the database
def save_jobs(jobs, keyword):
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
            print("Error inserting job:", e)
    conn.commit()
    conn.close()

def fetch_jobs(keyword=None):
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


# Initialize sent jobs table
def init_sent_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sent_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_link TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

# Mark job as sent
def mark_job_sent(job_link):
    init_sent_table()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO sent_jobs (job_link) VALUES (?)", (job_link,))
    conn.commit()
    conn.close()

# Check if job has already been sent
def job_already_sent(job_link):
    init_sent_table()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM sent_jobs WHERE job_link=? LIMIT 1", (job_link,))
    exists = c.fetchone() is not None
    conn.close()
    return exists
