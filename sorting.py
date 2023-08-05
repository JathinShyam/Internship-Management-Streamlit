import streamlit as st
import sqlite3
import pandas as pd


   
def view_applications_old():
    conn = sqlite3.connect("internship_applications.db")

    st.subheader("View Applications")

    # Input fields for filtering applications

    filter_cgpa = st.number_input("Filter by CGPA", min_value=0.0, max_value=10.0, step=0.1)
    year_of_studying_options = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduated"]
    year_of_studying = st.selectbox("Year of Studying:", year_of_studying_options)
    filter_skills = st.text_input("Filter by Skills")

    # SQL query for filtering applications
    query = "SELECT * FROM applications WHERE 1=1"
    # if filter_year:
    #     query += f" AND year_of_studying = {year_of_studying}"
    if filter_cgpa:
        query += f" AND gpa >= {filter_cgpa}"
    if year_of_studying:
            query += f" AND year_of_studying = '{year_of_studying}'"
    if filter_skills:
        query += f" AND skills LIKE '%{filter_skills}%'"

    # Input field for sorting applications
    sort_by = st.selectbox("Sort Applications by", [ "GPA", "Year of Studying"])

    # # SQL query for sorting applications
    if sort_by == "GPA":
        query += " ORDER BY gpa DESC"
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
  