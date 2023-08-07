import streamlit as st
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage





# Email settings (for demonstration purposes)
SMTP_SERVER = "smtp.gmail.com"  # Replace with your SMTP server address
SMTP_PORT = 587  # Replace with your SMTP server port number
SMTP_USERNAME = "abc@gmail.com"  # Replace with your email account's username or email address
SMTP_PASSWORD = "password"  # Replace with your email account's password



def send_email_to_student(email, name):
    message = f"Dear {name},\n\nCongratulations! You have been selected for the internship due to your skills.\n\nBest regards,\nThe Internship Team"
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, email, message)
        st.success(f"Email sent successfully to {name}!")
    except smtplib.SMTPAuthenticationError:
        st.error("Failed to authenticate with the SMTP server. Please check your SMTP username and password.")
    except smtplib.SMTPException as e:
        st.error(f"Failed to send email to {name}. Error: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred. Error: {str(e)}")





# Function to send an email
def send_email(to_email, subject, body):
    from_email = "kshyamrdy@gmail.com"  # Replace with your email address
    password = "zpgyocbbtusdvjln"  # Replace with your email password

    msg=EmailMessage()
    msg.set_content(body)

    # msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server address and port
    server.starttls()
    server.login(from_email, password)
    server.send_message(msg)
    # server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
