import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
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

def save_jobs(jobs, keyword):
    """
    Save a list of jobs to the database.
    """
    for job in jobs:
        try:
            cursor.execute("""
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

def fetch_jobs(keyword=None):
    """
    Fetch jobs from the database.
    If keyword is provided, filter by keyword.
    """
    if keyword:
        cursor.execute("SELECT title, company, location, link FROM jobs WHERE keyword=?", (keyword,))
    else:
        cursor.execute("SELECT title, company, location, link FROM jobs")
    return cursor.fetchall()
