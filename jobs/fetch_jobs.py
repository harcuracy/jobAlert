import os
from apify_client import ApifyClient
from dotenv import load_dotenv
from db import save_jobs  

load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

client = ApifyClient(APIFY_TOKEN)
ACTOR_ID = "muhammetakkurtt~naukri-job-scraper"

def scrape_jobs(keyword="software developer", max_jobs=10):
    """
    Scrape jobs via Apify and return the list of jobs.
    """
    run_input = {
        "keyword": keyword,
        "maxJobs": max_jobs,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
    }

    # Run the actor
    run = client.actor(ACTOR_ID).call(run_input=run_input)

    jobs = []
    for item in client.dataset(run.get("defaultDatasetId")).iterate_items():
        job = {
            "title": item.get("title") or item.get("jobTitle"),
            "company": item.get("company") or item.get("companyName"),
            "location": item.get("location") or item.get("jobLocation"),
            "link": item.get("url") or item.get("jobUrl") or item.get("listingUrl"),
        }
        if job["title"] and job["company"] and job["link"]:
            jobs.append(job)

    # Save to database
    save_jobs(jobs, keyword)
    return jobs

# Example usage
if __name__ == "__main__":
    jobs = scrape_jobs("data scientist", max_jobs=50)
    print(f"Saved {len(jobs)} jobs to the database.")
    for j in jobs:
        print(j)
