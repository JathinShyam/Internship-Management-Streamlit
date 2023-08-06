import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import smtplib
import hashlib
from new import *

# Hardcoded login credentials (for demonstration purposes)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"




def create_table():
    conn = sqlite3.connect("internship_applications.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (name TEXT, email TEXT, university TEXT, major TEXT, year_of_studying TEXT, semester INTEGER,
                 gpa REAL, skills TEXT, why_internship TEXT, interested_in_full_time INTEGER, resume BLOB)''')
    conn.commit()
    conn.close()

# def create_table_new():
#     worksheet = authenticate_google_sheets()
#     headers = ['name', 'email', 'university', 'major', 'year_of_studying', 'semester', 'gpa', 'skills', 'why_internship', 'interested_in_full_time', 'resume']
#     worksheet.append_row(headers)

def create_users_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Retrieve the hashed password for the given username from the database
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()

    if result is None:
        return False
    else:
        # Check if the hashed password matches the provided password
        hashed_password = result[0]
        if hashed_password == hash_password(password):
            return True
        else:
            return False

