import os

# Define the folder and file structure directly at root
structure = {
    "config": ["__init__.py", "settings.py"],
    "jobs": ["__init__.py", "fetch_jobs.py", "parse_jobs.py"],
    "llm": ["__init__.py", "formatter.py"],
    "notifications": ["__init__.py", "whatsapp.py", "email.py", "sms.py"],
    "templates": [
        "whatsapp_single_job.txt",
        "email_single_job.html",
        "sms_single_job.txt"
    ],
    "utils": ["__init__.py", "logger.py", "helpers.py"],
    "data": ["students.csv", "jobs_cache.json"],
    "tests": ["test_whatsapp.py", "test_email.py"],
    # top-level files (no folder)
    ".": ["app.py", "README.md"]
}

def create_structure(base_path, structure_dict):
    for folder, files in structure_dict.items():
        if folder == ".":
            # create top-level files directly in base_path
            for file_name in files:
                file_path = os.path.join(base_path, file_name)
                if not os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        if file_name.endswith(".py"):
                            f.write(f"# {file_name}\n")
                        else:
                            f.write("")
        else:
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                if not os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        if file_name.endswith(".py"):
                            f.write(f"# {file_name}\n")
                        else:
                            f.write("")

if __name__ == "__main__":
    base_dir = "."  # current directory
    create_structure(base_dir, structure)
    print("✅ Project structure created successfully.")
# Create the directory structure and files