import os
import smtplib
from email.mime.text import MIMEText
import mysql.connector


# Database connection details
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Email details
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

email_subject = 'Release Notes for the Latest Version of MyTradingTracker'

# Path to release notes file
release_notes_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources', 'releasenotes.html')

# Connect to the database
connection = mysql.connector.connect(host=DB_HOST,
                                        port=DB_PORT,
                                        database=DB_NAME,
                                        user=DB_USERNAME,
                                        password=DB_PASSWORD)

cursor = connection.cursor(dictionary=True)

# Query distinct email addresses from user table
cursor.execute("SELECT DISTINCT email FROM user where email_optin = 1")
result = cursor.fetchall()

email_addresses = result

# Read release notes from file
with open(release_notes_file, 'r') as file:
    release_notes = file.read()

# Loop through email addresses and send release notes
for email_address in email_addresses:
    email_body = release_notes
    message = MIMEText(email_body, 'html')
    message['Subject'] = email_subject
    message['From'] = SMTP_USERNAME
    message['To'] = email_address['email']

    # Send the email
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, email_address['email'], message.as_string())

# Close the database connection
cursor.close()
connection.close()
