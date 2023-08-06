import streamlit as st
import sqlite3
import pandas as pd
from emailing import *
from inserting_data import *
import base64

   
def filtering_sorting():

    # global conn
    # if not conn:
    #     conn = create_connection("internship_applications.db")

    conn = sqlite3.connect("internship_applications.db")

    st.subheader("View Applications")

    # Input fields for filtering applications

    filter_cgpa = st.number_input("Filter by CGPA", min_value=0.0, max_value=10.0, step=0.1)
    year_of_studying_options = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduated"]
    year_of_studying = st.selectbox("Year of Studying:", year_of_studying_options)
    filter_skills = st.text_input("Filter by Skills")

    # SQL query for filtering applications
    query = "SELECT * FROM applications WHERE 1=1"
    
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
    conn.close()

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

            # # View the resume in PDF format
            # st.write("### Resume:")
            # st.write(f"**File Name:** {row['name']}_Resume.pdf")  # Display the file name for the resume
            # if row['resume']:  # Check if the resume is not empty before displaying
            #     st.download_button(label="Download Resume PDF", data=row['resume'], file_name=f"{row['name']}_Resume.pdf", mime="application/pdf")
            # else:
            #     st.write("No resume uploaded.")


            # View the resume in PDF format
            st.write("### Resume:")
            st.write(f"**File Name:** {row['name']}_Resume.pdf")  # Display the file name for the resume
            if row['resume']:  # Check if the resume is not empty before displaying
                download_url = get_download_link(row['resume'], f"{row['name']}_Resume.pdf", "Download Resume PDF")
                st.markdown(download_url, unsafe_allow_html=True)
            else:
                st.write("No resume uploaded.")


            if row['email']:
                if st.button(f"Send Email {idx}"):  # Use idx as a part of the key for the button
                    send_email(row['email'], f"Regarding Your Internship Application", f"Dear {row['name']},\n\nWe have reviewed your internship application and would like to thank you for applying. Your application has been received and is currently under review.\n\nBest Regards,\nThe Internship Team")
                    st.success("Email sent successfully!")
                    
            st.write("---")

    
  
# Helper function to create a download link
def get_download_link(data, filename, text):
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'
    return href






# def filtering_sorting():
#     # Input fields for filtering applications
#     with st.form("filter_form"):
#         filter_cgpa = st.number_input("Filter by CGPA", min_value=0.0, max_value=10.0, step=0.1)
#         year_of_studying_options = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduated"]
#         year_of_studying = st.selectbox("Year of Studying:", year_of_studying_options)
#         filter_skills = st.text_input("Filter by Skills")

#         filter_button_clicked = st.form_submit_button("Filter")

#     # SQL query for filtering applications
#     if filter_button_clicked:
#         query = "SELECT * FROM applications WHERE 1=1"

#         if filter_cgpa:
#             query += f" AND gpa >= {filter_cgpa}"
#         if year_of_studying:
#             query += f" AND year_of_studying = '{year_of_studying}'"
#         if filter_skills:
#             query += f" AND skills LIKE '%{filter_skills}%'"

#         # Input field for sorting applications
#         sort_by = st.selectbox("Sort Applications by", ["GPA", "Year of Studying"])

#         # # SQL query for sorting applications
#         if sort_by == "GPA":
#             query += " ORDER BY gpa DESC"
#         # elif sort_by == "Year of Studying":
#         #     query += " ORDER BY year_of_studying"

#         # Execute the query and fetch the filtered and sorted applications
#         conn = sqlite3.connect("internship_applications.db")
#         df = pd.read_sql_query(query, conn)
#         conn.close()

#         if df.empty:
#             st.warning("No applications found matching the filter criteria.")
#         else:
#             for idx, row in df.iterrows():
#                 # Display application details
#                 st.write(f"### Application from {row['name']}")
#                 st.write(f"**Email:** {row['email']}")
#                 st.write(f"**University:** {row['university']}")
#                 st.write(f"**Major:** {row['major']}")
#                 st.write(f"**Year of Studying:** {row['year_of_studying']}")
#                 st.write(f"**Semester:** {row['semester']}")
#                 st.write(f"**GPA:** {row['gpa']:.2f}")
#                 st.write(f"**Skills:** {row['skills']}")
#                 st.write(f"**Why Internship:** {row['why_internship']}")
#                 st.write(f"**Interested in Full Time:** {'Yes' if row['interested_in_full_time'] else 'No'}")

#                 # View the resume in PDF format
#                 st.write("### Resume:")
#                 st.write(f"**File Name:** {row['name']}_Resume.pdf")  # Display the file name for the resume
#                 if row['resume']:  # Check if the resume is not empty before displaying
#                     download_url = get_download_link(row['resume'], f"{row['name']}_Resume.pdf", "Download Resume PDF")
#                     st.markdown(download_url, unsafe_allow_html=True)
#                 else:
#                     st.write("No resume uploaded.")

#                 if row['email']:
#                     if st.button(f"Send Email {idx}"):  # Use idx as a part of the key for the button
#                         send_email(row['email'], f"Regarding Your Internship Application",
#                                 f"Dear {row['name']},\n\nWe have reviewed your internship application and would like to thank you for applying. Your application has been received and is currently under review.\n\nBest Regards,\nThe Internship Team")
#                         st.success("Email sent successfully!")

#                 st.write("---")

