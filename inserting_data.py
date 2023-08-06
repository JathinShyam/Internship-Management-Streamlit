import streamlit as st
import sqlite3
import re
import os
from sqlite3 import Error

def is_valid_email(email):
    # Regex pattern for email validation
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

# Global variable for the connection
conn = None

# Function to create a database connection and initialize connection pool
def create_connection(database_file):
    global conn
    if not conn:
        try:
            conn = sqlite3.connect(database_file)
        except Error as e:
            print(e)
            return None
    return conn

# Function to execute SQL query with transaction
def execute_query_with_transaction(conn, query, data):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
        return True
    except Error as e:
        print(e)
        return False

# Modified insert_data function
def insert_data(name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume):
    global conn
    if not conn:
        conn = create_connection("internship_applications.db")
    if not name or not email or not university or not major or not year_of_studying or not semester or not gpa or not resume:
        st.error("Please fill in all mandatory fields and upload your resume.")
    elif not is_valid_email(email):
        st.error("Please enter a valid email")
    else:

        # Convert the resume file to bytes and store it in a folder
        resume_bytes = resume.read()
        resume_folder = "resumes"
        os.makedirs(resume_folder, exist_ok=True)
        resume_filename = os.path.join(resume_folder, f"{name}_Resume.pdf")
        with open(resume_filename, "wb") as file:
            file.write(resume_bytes)

        # Sample query
        query = "INSERT INTO applications (name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume_bytes)
        
        # Execute query with transaction
        if execute_query_with_transaction(conn, query, data):
            conn.commit() #Committing the transaction
            st.success("Application submitted successfully!")
        else:
            st.error("Failed to submit application.")
        conn.close()  #Closing the connection



# def insert_data(name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume):
#     if not name or not email or not university or not major or not year_of_studying or not semester or not gpa  or not resume:
#        st.error("Please fill in all mandatory fields and upload your resume.")

#     elif not is_valid_email(email):
#         st.error("Please enter a valid email")
#     else:
#         conn = sqlite3.connect("internship_applications.db")
#         c = conn.cursor()

#         # Convert the resume file to bytes and store it in a folder
#         resume_bytes = resume.read()
#         resume_folder = "resumes"
#         os.makedirs(resume_folder, exist_ok=True)
#         resume_filename = os.path.join(resume_folder, f"{name}_Resume.pdf")
#         with open(resume_filename, "wb") as file:
#             file.write(resume_bytes)

#         c.execute("INSERT INTO applications (name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
#                   (name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume_bytes))
#         conn.commit()
#         conn.close()
#         st.success("Application submitted successfully!")


import gspread
from google.oauth2.service_account import Credentials
from cachetools import cached, TTLCache

# Caching the authentication function for 1 hour
@cached(cache=TTLCache(maxsize=1, ttl=3600))
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("creds.json", scopes=scope)
    return gspread.authorize(creds)




# def insert_data(name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume):
#     try:
#         worksheet = authenticate_google_sheets().open("CRMProject").Sheet1
#     except gspread.exceptions.APIError as e:
#         print("Error accessing Google Sheets API. Please try again later.")
#         return

#     row = [name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume]
#     worksheet.append_row(row)

#     print("Application submitted successfully!")


# def create_table_sheets():
#     try:
#         worksheet = authenticate_google_sheets().open("CRMProject").sheet1
#         # Check if the table already exists by trying to read cell A1
#         worksheet.cell(1, 1).value
#     except gspread.exceptions.APIError as e:
#         print("Error accessing Google Sheets API. Please try again later.")
#         return
#     except gspread.exceptions.CellNotFound:
#         # If cell A1 is not found, it means the table doesn't exist, so create it
#         worksheet.update('A1', 'Name')
#         worksheet.update('B1', 'Email')
#         worksheet.update('C1', 'University')
#         worksheet.update('D1', 'Major')
#         worksheet.update('E1', 'Year of Studying')
#         worksheet.update('F1', 'Semester')
#         worksheet.update('G1', 'GPA')
#         worksheet.update('H1', 'Skills')
#         worksheet.update('I1', 'Why Internship')
#         worksheet.update('J1', 'Interested in Full Time')
#         worksheet.update('K1', 'Resume')

#         print("Table created successfully!")
#     else:
#         print("Table already exists.")


# def insert_data_sheets(name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume):
#     try:
#         worksheet = authenticate_google_sheets().open("CRMProject").sheet1
#     except gspread.exceptions.APIError as e:
#         print("Error accessing Google Sheets API. Please try again later.")
#         return
#     # Convert the resume file to bytes and store it in a folder
#     resume_bytes = resume.read()
#     resume_folder = "resumes"
#     os.makedirs(resume_folder, exist_ok=True)
#     resume_filename = os.path.join(resume_folder, f"{name}_Resume.pdf")
#     with open(resume_filename, "wb") as file:
#         file.write(resume_bytes)
#     row = [name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume]
#     worksheet.append_row(row)

#     print("Application submitted successfully!")
