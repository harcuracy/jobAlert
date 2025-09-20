# test_fetch.py
from db import fetch_jobs

jobs = fetch_jobs("data scientist")  
print(f"Found {len(jobs)} jobs in DB:")
for title, company, location, link in jobs[:10]:  # first 10
    print(title, "|", company, "|", location, "|", link)
