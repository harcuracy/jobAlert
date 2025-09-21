#  read csv file

import os
import csv


def read_students(csv_file):
    students = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({
                "name": row["name"],
                "email": row["email"],
                "phone" : row["phone"],
                "department": row["department"],
                "skills": row.get("skills", "")
            })
    return students