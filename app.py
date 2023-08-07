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
from sorting import *
from modelling import *
st.set_page_config(layout="wide")


import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check if the 'logs' directory exists, if not create it
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up a file handler to log messages to a file
file_handler = logging.FileHandler('logs/app.log')
file_handler.setLevel(logging.INFO)

# Create a formatter for the file handler
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Add the file handler to the root logger
logging.getLogger().addHandler(file_handler)




def main():
    create_table()
    # create_table_new()
    create_users_table()


    st.title("Student Internship Application Management")

    menu_selection = st.sidebar.selectbox("Select an option:", 
                                          ["Home", "Submit Application", "View Applications", "Create New User", "Filtering"])

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
    
    elif menu_selection=="Filtering":

        # # User Authentication
        # st.subheader("Login to Access View Applications")
        # username = st.text_input("Username")
        # password = st.text_input("Password", type="password")

        # if st.button("Login"):
        #     if username==VALID_USERNAME and password==VALID_PASSWORD:
        #         st.success(f"Welcome, {username}! You can now access the View Applications section.")
        #         filtering_sorting() 
        #     elif authenticate_user(username, password):
        #         st.success(f"Welcome, {username}! You can now access the View Applications section.")
        #         filtering_sorting()
        #     else:
        #         st.error("Invalid username or password. Please try again.")

        filtering_sorting()
        


if __name__ == "__main__":
    main()
