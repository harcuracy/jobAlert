#  read csv file

import os
import csv
import io


def read_students(csv_file):
    """Reads students from a Streamlit UploadedFile or a normal CSV file path."""
    students = []

    # ✅ Handle Streamlit UploadedFile (in-memory file)
    if hasattr(csv_file, "read"):
        csv_file.seek(0)
        content = csv_file.getvalue().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
    else:
        # ✅ Handle normal file path
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

    for row in reader:
        students.append({
            "name": row.get("name", "").strip(),
            "email": row.get("email", "").strip(),
            "phone": row.get("phone", "").strip(),
            "department": row.get("department", "").strip(),
            "skills": row.get("skills", "").strip()
        })

    return students