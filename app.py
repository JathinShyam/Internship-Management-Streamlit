# app.py
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import smtplib
#import pdb
import os
from inserting_data import *
from displaying_applications import *
from creating_new_user import *
from sorting import view_applications_old
from modelling import *
st.set_page_config(layout="wide")


# Email settings (for demonstration purposes)
SMTP_SERVER = "smtp.example.com"  # Replace with your SMTP server address
SMTP_PORT = 587  # Replace with your SMTP server port number
SMTP_USERNAME = "your_username"  # Replace with your email account's username or email address
SMTP_PASSWORD = "your_password"  # Replace with your email account's password



def send_email_to_student(email, name):
    message = f"Dear {name},\n\nCongratulations! You have been selected for the internship due to your high GPA.\n\nBest regards,\nThe Internship Team"
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, email, message)
        st.success(f"Email sent successfully to {name}!")
    except Exception as e:
        st.error(f"Failed to send email to {name}. Error: {str(e)}")



def main():
    create_table()
    create_users_table()

    st.title("Student Internship Application Management")

    menu_selection = st.sidebar.selectbox("Select an option:", 
                                          ["Home", "Submit Application", "View Applications", "Create New User", "View Applications New"])

    if menu_selection == "Home":
        st.header("Welcome to the Internship Application Management App!")
        st.write("Please use the navigation sidebar to access different features.")

    elif menu_selection == "Submit Application":

        st.header("Student Internship Application Form")
        st.write("Please fill in the following details to apply for the internship:")

        # Input fields
        name = st.text_input("Name:", max_chars=30)
        email = st.text_input("Email:")
        university = st.text_input("University:", max_chars=30)
        major = st.text_input("Major:", max_chars=30)
        
        # Dropdown for the year of studying
        year_of_studying_options = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduated"]
        year_of_studying = st.selectbox("Year of Studying:", year_of_studying_options)

        semester = st.number_input("Current Semester:", min_value=1, max_value=8, step=1)
        gpa = st.number_input("GPA (on a scale of 10):", min_value=0.0, max_value=10.0, step=0.1)
        skills = st.text_area("Skills (comma-separated):", max_chars=100)
        why_internship = st.text_area("Why do you want this internship?", max_chars=100)
        
        # Boolean field for full-time interest
        interested_in_full_time = st.checkbox("Are you interested in a full-time position?")

        # File uploader for resume
        resume_file = st.file_uploader("Upload your resume (PDF or DOCX):", type=["pdf", "docx"])

        if st.button("Submit"):
            insert_data(name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume_file)
            

        
    elif menu_selection == "View Applications":
        # User Authentication
        st.subheader("Login to Access View Applications")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username==VALID_USERNAME and password==VALID_PASSWORD:
                st.success(f"Welcome, {username}! You can now access the View Applications section.")
                display_applications() 
            elif authenticate_user(username, password):
                st.success(f"Welcome, {username}! You can now access the View Applications section.")
                display_applications()
            else:
                st.error("Invalid username or password. Please try again.")


    elif menu_selection == "Create New User":
        create_new_user()
    
    elif menu_selection=="View Applications New":
        view_applications_old()


if __name__ == "__main__":
    main()
