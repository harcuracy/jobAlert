from jobs.fetch_jobs import scrape_jobs


if __name__ == "__main__":
    departments = [
        "Data Scientist",
        "Software Engineer",
        "Medical Laboratory Scientist",
        "Biochemist",
        "Computer Science"
    ]

    for dep in departments:
        jobs = scrape_jobs(dep + " jobs", max_jobs=50)
        print(f"Saved {len(jobs)} jobs for {dep} to the database.")
