# app.py
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import smtplib
from email_validator import validate_email, EmailNotValidError
from email.mime.text import MIMEText
import re
import pdb


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

# def is_valid_email(email):
#     # Regex pattern for email validation
#     pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
#     return re.match(pattern, email)


def insert_data(name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume):
    if not name or not email or not university or not major or not year_of_studying or not semester or not gpa or not skills or not resume:
        st.error("Please fill in all mandatory fields and upload your resume.")
    else:
        conn = sqlite3.connect("internship_applications.db")
        c = conn.cursor()
        c.execute("INSERT INTO applications (name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, email, university, major, year_of_studying, semester, gpa, skills, why_internship, interested_in_full_time, resume))
        conn.commit()
        conn.close()
        st.success("Application submitted successfully!")



# def create_new_user(username, password):
#     conn = sqlite3.connect("users.db")
#     c = conn.cursor()
#     c.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
#     conn.commit()
#     conn.close()


def create_new_user():
    st.subheader("Create New User")

    # Input fields for creating a new user
    username = st.text_input("Username (mandatory)", max_chars=100)
    password = st.text_input("Password (mandatory)", max_chars=100, type="password")

    if st.button("Create User"):
        if not username or not password:
            st.error("Please fill in both username and password.")
        else:
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


def display_applications():
    conn = sqlite3.connect("internship_applications.db")
    df = pd.read_sql_query("SELECT * FROM applications", conn)
    conn.close()

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
    ax2.set_xticks(range(1, 11))  # Use range from 1 to 10 (inclusive) for GPA
    ax2.set_xticklabels([f"{i:.1f}" for i in range(1, 11)])  # Set labels for GPA
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Additional Visualizations")
    
    # Count plot for the distribution of year of studying
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="year_of_studying")
    ax.set_xlabel("Year of Studying")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Year of Studying")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    st.pyplot(fig)

    # Count plot for the distribution of full-time interest
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="interested_in_full_time")
    ax.set_xlabel("Interested in Full Time")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Interest in Full Time")
    ax.set_xticks([0, 1])  # Explicitly set the tick positions to 0 and 1
    ax.set_xticklabels(["No", "Yes"])  # Set custom labels for each tick position
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    st.pyplot(fig)

    # Display the table with all applications
    st.subheader("Submitted Applications")
    st.dataframe(df)


    with st.expander("View Resumes (PDF)"):
        for idx, row in df.iterrows():
            st.write(f"### Application from {row['name']}")
            st.write(f"**Email:** {row['email']}")
            st.write(f"**University:** {row['university']}")
            st.write(f"**Major:** {row['major']}")
            st.write(f"**Year of Studying:** {row['year_of_studying']}")
            st.write(f"**Semester:** {row['semester']}")
            st.write(f"**GPA:** {row['gpa']:.2f}")
            st.write(f"**Skills:** {row['skills']}")
            st.write(f"**Why Internship:** {row['why_internship']}")
            st.write(f"**Interested in Full Time:** {'Yes' if row['interested_in_full_time'] else 'No'}")

            # View the resume in PDF format
            st.write("### Resume:")
            st.write(f"**File Name:** {row['name']}_Resume.pdf")  # Display the file name for the resume
            if row['resume']:  # Check if the resume is not empty before displaying
                st.download_button(label="Download Resume PDF", data=row['resume'], file_name=f"{row['name']}_Resume.pdf", mime="application/pdf")
            else:
                st.write("No resume uploaded.")

            st.write("---")

    
def view_applications_old():
    conn = sqlite3.connect("internship_applications.db")

    st.subheader("View Applications")

    # Input fields for filtering applications
    filter_year = st.number_input("Filter by Year of Studying", min_value=1, max_value=5)
    filter_cgpa = st.number_input("Filter by CGPA", min_value=0.0, max_value=10.0, step=0.1)
    #filter_skills = st.text_input("Filter by Skills")
    pdb.set_trace()
    # SQL query for filtering applications
    query = "SELECT * FROM applications WHERE 1=1"
    if filter_year:
        query += f" AND year_of_studying = {filter_year}"
    if filter_cgpa:
        query += f" AND gpa >= {filter_cgpa}"
    # if filter_skills:
    #     query += f" AND skills LIKE '%{filter_skills}%'"

    # Input field for sorting applications
    # sort_by = st.selectbox("Sort Applications by", ["Name", "GPA", "Year of Studying"])

    # # SQL query for sorting applications
    # if sort_by == "Name":
    #     query += " ORDER BY name"
    # elif sort_by == "GPA":
    #     query += " ORDER BY gpa DESC"
    # elif sort_by == "Year of Studying":
    #     query += " ORDER BY year_of_studying"

    # Execute the query and fetch the filtered and sorted applications
    df = pd.read_sql_query(query, conn)

    if df.empty:
        st.warning("No applications found matching the filter criteria.")
    else:
        for idx, row in df.iterrows():
            # Display application details
            st.write(f"### Application from {row['name']}")
            st.write(f"**Email:** {row['email']}")
            st.write(f"**University:** {row['university']}")
            st.write(f"**Major:** {row['major']}")
            st.write(f"**Year of Studying:** {row['year_of_studying']}")
            st.write(f"**Semester:** {row['semester']}")
            st.write(f"**GPA:** {row['gpa']:.2f}")
            st.write(f"**Skills:** {row['skills']}")
            st.write(f"**Why Internship:** {row['why_internship']}")
            st.write(f"**Interested in Full Time:** {'Yes' if row['interested_in_full_time'] else 'No'}")

            # View the resume in PDF format
            st.write("### Resume:")
            st.write(f"**File Name:** {row['name']}_Resume.pdf")  # Display the file name for the resume
            if row['resume']:  # Check if the resume is not empty before displaying
                st.download_button(label="Download Resume PDF", data=row['resume'], file_name=f"{row['name']}_Resume.pdf", mime="application/pdf")
            else:
                st.write("No resume uploaded.")

            st.write("---")

    conn.close()
  


def view_applications_new():
    conn = sqlite3.connect("internship_applications.db")

    st.subheader("View Applications")

    # Input fields for filtering applications
    filter_year = st.number_input("Filter by Year of Studying", min_value=1, max_value=5)
    filter_cgpa = st.number_input("Filter by CGPA", min_value=0.0, max_value=10.0, step=0.1)
    filter_skills = st.text_input("Filter by Skills")

    # SQL query for filtering applications
    query = "SELECT * FROM applications WHERE 1=1"
    if filter_year:
        query += f" AND year_of_studying = {filter_year}"
    if filter_cgpa:
        query += f" AND gpa >= {filter_cgpa}"
    if filter_skills:
        query += f" AND skills LIKE '%{filter_skills}%'"

    # Input field for sorting applications
    sort_by_options = ["Name", "GPA", "Year of Studying"]
    sort_by = st.multiselect("Sort Applications by", sort_by_options)

    # SQL query for sorting applications
    if sort_by:
        query += f" ORDER BY {', '.join(sort_by)}"

    # Execute the query and fetch the filtered and sorted applications
    df = pd.read_sql_query(query, conn)

    if df.empty:
        st.warning("No applications found matching the filter criteria.")
    else:
        for idx, row in df.iterrows():
            # Display application details
            st.write(f"### Application from {row['name']}")
            st.write(f"**Email:** {row['email']}")
            st.write(f"**University:** {row['university']}")
            st.write(f"**Major:** {row['major']}")
            st.write(f"**Year of Studying:** {row['year_of_studying']}")
            st.write(f"**Semester:** {row['semester']}")
            st.write(f"**GPA:** {row['gpa']:.2f}")
            st.write(f"**Skills:** {row['skills']}")
            st.write(f"**Why Internship:** {row['why_internship']}")
            st.write(f"**Interested in Full Time:** {'Yes' if row['interested_in_full_time'] else 'No'}")

            # View the resume in PDF format
            st.write("### Resume:")
            st.write(f"**File Name:** {row['name']}_Resume.pdf")  # Display the file name for the resume
            if row['resume']:  # Check if the resume is not empty before displaying
                st.download_button(label="Download Resume PDF", data=row['resume'], file_name=f"{row['name']}_Resume.pdf", mime="application/pdf")
            else:
                st.write("No resume uploaded.")

            st.write("---")

    conn.close()







def main():
    create_table()

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
            st.success("Application submitted successfully!")


    elif menu_selection == "View Applications":
        st.header("View Submitted Applications")
        # skill_filter = st.text_input("Filter by Skill (Optional)")
        login_username = st.text_input("Username:")
        login_password = st.text_input("Password:", type="password")

        if st.button("Login"):
            if login_username == VALID_USERNAME and login_password == VALID_PASSWORD:
                display_applications()
            else:
                st.error("Invalid username or password. Please try again.")
        

    elif menu_selection == "Create New User":
        create_new_user()
    
    elif menu_selection=="View Applications New":
        view_applications_old()


if __name__ == "__main__":
    main()
