import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from emailing import *
import math
from inserting_data import *
from sorting import *


def display_applications():

    conn = create_connection("internship_applications.db")
    query = "SELECT * FROM applications WHERE 1=1"
    df = pd.read_sql_query(query, conn)
    conn.close()

    st.subheader("Applications Overview")


    # Data preparation for the pie chart
    labels = ["Interested in Full Time", "Not Interested in Full Time"]
    sizes = [df["interested_in_full_time"].sum(), len(df) - df["interested_in_full_time"].sum()]
    # Create the first subplot for the pie chart
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax1.set_title("Interest in Full-Time")


    # Data preparation for the bar chart of GPA distribution
    gpa_counts = df["gpa"].value_counts().sort_index()
    # Create the second subplot for the bar chart
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.bar(gpa_counts.index, gpa_counts.values, width=0.4)
    ax2.set_title("GPA Distribution")
    ax2.set_xlabel("GPA")
    ax2.set_ylabel("Count")
    ax2.set_xticks(range(1, 11))  # Use range from 1 to 10 (inclusive) for GPA
    ax2.set_xticklabels([f"{i:.1f}" for i in range(1, 11)])  # Set labels for GPA
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability


    # Count plot for the distribution of year of studying
    fig3, ax3 = plt.subplots()
    sns.countplot(data=df, x="year_of_studying")
    ax3.set_xlabel("Year of Studying")
    ax3.set_ylabel("Count")
    ax3.set_title("Distribution of Year of Studying")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability



    # Count plot for the distribution of full-time interest
    fig4, ax4 = plt.subplots()
    sns.countplot(data=df, x="interested_in_full_time")
    ax4.set_xlabel("Interested in Full Time")
    ax4.set_ylabel("Count")
    ax4.set_title("Distribution of Interest in Full Time")
    ax4.set_xticks([0, 1])  # Explicitly set the tick positions to 0 and 1
    ax4.set_xticklabels(["No", "Yes"])  # Set custom labels for each tick position
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability


    # Create a two-column layout for the graphs
    col1, col2 = st.columns(2)

    # Display Graph 1 in the first column
    with col1:
        st.pyplot(fig1)

    # Display Graph 2 in the second column
    with col2:
        st.pyplot(fig2)

    # Display Graph 3 in the first column
    with col1:
        # Replace the following line with your code for Graph 3
        st.pyplot(fig3)
        pass
        

    # Display Graph 4 in the second column
    with col2:
        # Replace the following line with your code for Graph 4
        st.pyplot(fig4)
        pass
        

    # Display the table with all applications
    st.subheader("Submitted Applications")
    st.dataframe(df[:-1])


    with st.expander("View Resumes (PDF)"):

        # if st.button("Filter"):

        #     filter_cgpa = st.number_input("Filter by CGPA", min_value=0.0, max_value=10.0, step=0.1)
        #     year_of_studying_options = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduated"]
        #     year_of_studying = st.selectbox("Year of Studying:", year_of_studying_options)
        #     filter_skills = st.text_input("Filter by Skills")

        #     # SQL query for filtering applications
        #     query = "SELECT * FROM applications WHERE 1=1"
        #     if filter_cgpa:
        #         query += f" AND gpa >= {filter_cgpa}"
        #     if year_of_studying:
        #             query += f" AND year_of_studying = '{year_of_studying}'"
        #     if filter_skills:
        #         query += f" AND skills LIKE '%{filter_skills}%'"

        #     conn = sqlite3.connect("internship_applications.db")
        #     df = pd.read_sql_query(query, conn)
        #     conn.close()
        # else:
        #     conn = sqlite3.connect("internship_applications.db")
        #     df = pd.read_sql_query("SELECT * FROM applications", conn)
        #     conn.close()

        # # Pagination
        # page_size = 5
        # num_pages = math.ceil(len(df) / page_size)

        # page_number = st.number_input("Page Number", min_value=1, max_value=num_pages, value=1)
        # start_idx = (page_number - 1) * page_size
        # end_idx = start_idx + (len(df) % page_size) + 1

        # for idx, row in df.iloc[start_idx:end_idx].iterrows():
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
                download_url = get_download_link(row['resume'], f"{row['name']}_Resume.pdf", "Download Resume PDF")
                st.markdown(download_url, unsafe_allow_html=True)
            else:
                st.write("No resume uploaded.")
            # if row['email']:
            #     if st.button(f"Send Email {idx}"):  # Use idx as a part of the key for the button
            #         # send_email(row['email'], f"Regarding Your Internship Application", f"Dear {row['name']},\n\nWe have reviewed your internship application and would like to thank you for applying. Your application has been received and is currently under review.\n\nBest Regards,\nThe Internship Team")
            #         # st.success("Email sent successfully!")
                    
            #         send_email_to_student(row["email"], row["name"])
            st.write("---")