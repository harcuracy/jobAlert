# app.py

import streamlit as st
import pandas as pd

from main import send_job_alerts
from db.db import fetch_jobs

st.title("Job Alert Sender 📢")

# Upload CSV of students
uploaded_file = st.file_uploader("Upload students CSV", type=["csv"])

if uploaded_file:
    st.success("File uploaded successfully!")
    
    
    students_df = pd.read_csv(uploaded_file)
    st.dataframe(students_df.head())

    if st.button("Send Job Alerts"):
        st.info("Sending job alerts...")
        jobs = fetch_jobs()  # fetch jobs from database
        send_job_alerts(jobs, csv_file=uploaded_file)
        st.success("✅ Job alerts sent!")
