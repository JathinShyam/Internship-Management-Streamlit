# app.py
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import smtplib
from email_validator import validate_email, EmailNotValidError
from email.mime.text import MIMEText

# Hardcoded login credentials (for demonstration purposes)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# Email settings (for demonstration purposes)
SMTP_SERVER = "smtp.example.com"  # Replace with your SMTP server address
SMTP_PORT = 587  # Replace with your SMTP server port number
SMTP_USERNAME = "your_username"  # Replace with your email account's username or email address
SMTP_PASSWORD = "your_password"  # Replace with your email account's password

def create_table():
    conn = sqlite3.connect("internship_applications.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (name TEXT, email TEXT, university TEXT, major TEXT, year_of_studying TEXT, semester INTEGER,
                 gpa REAL, skills TEXT, why_internship TEXT, interested_in_full_time INTEGER, resume BLOB)''')
    conn.commit()
    conn.close()

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def insert_data(name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume_file):
    if not is_valid_email(email):
        st.error("Invalid email. Please provide a valid email address.")
        return

    conn = sqlite3.connect("internship_applications.db")
    c = conn.cursor()
    c.execute('''INSERT INTO applications 
                 (name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume_file.read()))
    conn.commit()
    conn.close()

def create_new_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
    conn.commit()
    conn.close()

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



def display_applications(skill_filter=None):
    conn = sqlite3.connect("internship_applications.db")
    df = pd.read_sql_query("SELECT * FROM applications", conn)
    conn.close()

    if skill_filter:
        df = df[df["skills"].str.contains(skill_filter, case=False, na=False)]

    st.subheader("Applications Overview")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Pie chart
    labels = ["Interested in Full Time", "Not Interested in Full Time"]
    sizes = [df["interested_in_full_time"].sum(), len(df) - df["interested_in_full_time"].sum()]
    ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax1.set_title("Interest in Full-Time")

    # Bar chart of GPA distribution
    gpa_counts = df["gpa"].value_counts().sort_index()
    ax2.bar(gpa_counts.index, gpa_counts.values, width=0.4)
    ax2.set_title("GPA Distribution")
    ax2.set_xlabel("GPA")
    ax2.set_ylabel("Count")
    ax2.set_xticks(range(11))
    ax2.set_xticklabels([f"{i:.1f}" for i in range(11)])

    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Additional Visualizations")
    
    # Count plot for the distribution of year of studying
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="year_of_studying")
    ax.set_xlabel("Year of Studying")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Year of Studying")
    st.pyplot(fig)

    # Count plot for the distribution of full-time interest
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="interested_in_full_time")
    ax.set_xlabel("Interested in Full Time")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Interest in Full Time")
    ax.set_xticklabels(["No", "Yes"])
    st.pyplot(fig)

    # Display the table with filtered applications (if filtered)
    st.subheader("Submitted Applications")
    st.dataframe(df)



def main():
    create_table()

    st.title("Student Internship Application Form")
    st.write("Please fill in the following details to apply for the internship:")

    # Input fields
    name = st.text_input("Name:")
    email = st.text_input("Email:")
    university = st.text_input("University:")
    major = st.text_input("Major:")
    
    # Dropdown for the year of studying
    year_of_studying_options = ["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "6th Year", "Graduated"]
    year_of_studying = st.selectbox("Year of Studying:", year_of_studying_options)

    semester = st.number_input("Current Semester:", min_value=1, max_value=10, step=1)
    gpa = st.number_input("GPA (on a scale of 10):", min_value=0.0, max_value=10.0, step=0.1)
    skills = st.text_area("Skills (comma-separated):")
    why_internship = st.text_area("Why do you want this internship?")
    
    # Boolean field for full-time interest
    interested_in_full_time = st.checkbox("Are you interested in a full-time position?")

    # File uploader for resume
    resume_file = st.file_uploader("Upload your resume (PDF or DOCX):", type=["pdf", "docx"])

    if st.button("Submit"):
        insert_data(name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume_file)
        st.success("Application submitted successfully!")

    if st.button("View Applications"):
        # Display login form
        login_username = st.text_input("Username:")
        login_password = st.text_input("Password:", type="password")

        if st.button("Login"):
            if login_username == VALID_USERNAME and login_password == VALID_PASSWORD:
                display_applications()
            else:
                st.error("Invalid username or password. Please try again.")

    # New user registration section
    st.subheader("New User Registration")
    new_username = st.text_input("New Username:")
    new_password = st.text_input("New Password:", type="password")
    confirm_password = st.text_input("Confirm Password:", type="password")

    if st.button("Register"):
        if new_username and new_password and new_password == confirm_password:
            create_new_user(new_username, new_password)
            st.success("New user created successfully!")
        else:
            st.error("Please provide a valid username and matching passwords.")


if __name__ == "__main__":
    create_table()
    main()
