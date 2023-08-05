import streamlit as st
import sqlite3
import re
import os


def is_valid_email(email):
    # Regex pattern for email validation
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


def insert_data(name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume):
    if not name or not email or not university or not major or not year_of_studying or not semester or not gpa  or not resume:
       st.error("Please fill in all mandatory fields and upload your resume.")

    elif not is_valid_email(email):
        st.error("Please enter a valid email")
    else:
        conn = sqlite3.connect("internship_applications.db")
        c = conn.cursor()

        # Convert the resume file to bytes and store it in a folder
        resume_bytes = resume.read()
        resume_folder = "resumes"
        os.makedirs(resume_folder, exist_ok=True)
        resume_filename = os.path.join(resume_folder, f"{name}_Resume.pdf")
        with open(resume_filename, "wb") as file:
            file.write(resume_bytes)

        c.execute("INSERT INTO applications (name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume_bytes))
        conn.commit()
        conn.close()
        st.success("Application submitted successfully!")
