from jobs.fetch_jobs import get_jobs_from_naukri


if __name__ == "__main__":
    jobs = get_jobs_from_naukri("data scientist", max_jobs=50)
    print(f"Saved {len(jobs)} jobs to the database.")
    for j in jobs:
        print(j)
