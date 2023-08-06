import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import hashlib
from inserting_data import *



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



def create_new_user():
    st.subheader("Create New User")

    new_username = st.text_input("Username", value="", key="new_username")  # Assign a unique key for this widget
    new_password = st.text_input("Password", value="", type="password", key="new_password")  # Assign a unique key for this widget
    confirm_password = st.text_input("Confirm Password", value="", type="password", key="confirm_password")

    if st.button("Create User"):
        if new_username.strip() == "" or new_password.strip() == "":
            st.warning("Username and password cannot be empty.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            global conn
            if not conn:
                conn = create_connection("users.db")
            # conn = sqlite3.connect("users.db")
            c = conn.cursor()
            
            # Check if the username already exists
            c.execute("SELECT COUNT(*) FROM users WHERE username=?", (new_username,))
            result = c.fetchone()
            if result[0] > 0:
                st.error("Username is already taken. Please choose a different username.")
            else:
                # Hash the password before storing it in the database
                hashed_password = hash_password(new_password)
                
                # Insert the new user into the database
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, hashed_password))
                conn.commit()
                conn.close()

                st.success("User created successfully. You can now login with the new account.")

