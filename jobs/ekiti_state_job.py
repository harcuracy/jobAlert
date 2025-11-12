import random
from datetime import datetime
from db.db import save_jobs
# =========================
# 🎲 Dummy Job Generator
# =========================
def generate_dummy_jobs(n=50, location="Ekiti State"):
    companies = [
        "TechBridge Solutions", "Ekiti Agro Ventures", "Fountain Software Ltd",
        "GreenFarm Nigeria", "AdoTech Hub", "Harmony Schools", "Ekiti Medical Center",
        "Solid Foundation Microfinance", "PeakNet Services", "BrightFuture NGO",
        "SwiftWorks Ltd", "CrestPoint Energy", "Excel Tutors", "FarmPro Cooperative",
        "Skyline Logistics", "Innovate Africa", "Royal Mart Stores", "CoreTech Systems",
        "LifeCare Hospital", "SmartBuild Constructions"
    ]

    titles = [
        "Software Developer", "Frontend Engineer", "Backend Engineer",
        "Mobile App Developer", "Agricultural Extension Worker", "Marketing Officer",
        "Customer Service Representative", "Data Analyst", "Teacher", "Lecturer",
        "Administrative Assistant", "Accountant", "Project Manager", "Business Analyst",
        "Sales Executive", "Graphic Designer", "Social Media Manager", "Nurse",
        "Electrical Technician", "Mechanical Engineer", "Civil Engineer", "IT Support Officer",
        "Pharmacist", "Field Sales Agent", "Research Assistant"
    ]

    job_types = ["Full-time", "Part-time", "Remote", "Contract", "Internship"]
    salary_ranges = [
        "₦80,000 - ₦120,000", "₦100,000 - ₦150,000", "₦50,000 - ₦80,000",
        "₦150,000 - ₦250,000", "Negotiable"
    ]

    jobs = []
    for i in range(n):
        title = random.choice(titles)
        company = random.choice(companies)
        link = f"https://jobs.ekiti.ng/{title.lower().replace(' ', '-')}-{i+1}"
        jobs.append({
            "title": f"{title} ({random.choice(job_types)})",
            "company": company,
            "location": location,
            "link": link
        })
    return jobs


# =========================
# 💾 Save to Database
# =========================
if __name__ == "__main__":
    dummy_jobs = generate_dummy_jobs(50, location="Ekiti State")
    save_jobs(dummy_jobs, keyword="ekiti")
    print(f"✅ {len(dummy_jobs)} dummy jobs for Ekiti State saved successfully!")
