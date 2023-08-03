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


st.title("Student Internship Application Management")

st.header("Welcome to the Internship Application Management App!")
st.write("Please use the navigation sidebar to access different features.")


def create_table():
    conn = sqlite3.connect("internship_applications.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (name TEXT, email TEXT, university TEXT, major TEXT, year_of_studying TEXT, semester INTEGER,
                 gpa REAL, skills TEXT, why_internship TEXT, interested_in_full_time INTEGER, resume BLOB)''')
    conn.commit()
    conn.close()


create_table()