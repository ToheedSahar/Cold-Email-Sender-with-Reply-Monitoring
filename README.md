## Cold Email Sender with Reply Monitoring

## Overview
This Python script automates sending cold emails to Emails listed in an Excel file, monitors for replies, and sends follow-up emails if no reply is received within 60 hours. It uses Gmail for email operations, logs activities in an SQLite database, and provides desktop notifications for new replies.


## Features

Email Sending: Sends personalized cold emails from an Excel file.
Reply Monitoring: Checks for replies and logs them.
Follow-up Emails: Sends follow-ups if no reply is received after 60 hours.
Database Logging: Tracks sent emails and follow-up status in SQLite.
Notifications: Displays desktop and GUI notifications for new replies.
Retry Mechanism: Retries failed email sends up to three times.
Random Delays: Adds delays between emails to avoid spam flags.

## Prerequisites

Python 3.x
A Gmail account with an App Password (2-Step Verification required)
An Excel file named emails.xlsx with 'Gmail' and 'Name' columns

## Setup

Install Dependencies:
pip install -r requirements.txt

On some systems (e.g., Ubuntu), install tkinter separately:
sudo apt-get install python3-tk


## Email Configuration:

In cold_email.py, replace "your_email@gmail.com" and "your_app_password" with your Gmail address and App Password.
Security Note: Do not commit actual credentials to GitHub. Use placeholders and update them locally.


## Excel File:

Ensure emails.xlsx exists with valid 'Gmail' and 'Name' entries (no '-' or empty emails).


## Database:

The script creates email_log.db automatically. No setup needed.



## Usage

Run the Script:
python cold_email.py


Initial emails are sent in a background thread.
Reply monitoring runs in the main thread.


## Behavior:

Checks for replies hourly.
Shows notifications for new replies.
Sends follow-ups after 60 hours if no reply is detected.



## Important Notes

Credentials: Replace email placeholders locally. Never upload real credentials to GitHub.
App Password: Generate one in Google Account settings under Security > App Passwords.
Excel Format: Must include 'Gmail' and 'Channel Name' columns.
Database: Keep email_log.db intact during execution.
Delays: Random delays (96-97 minutes) are set to avoid spam detection. Adjust in the script if needed.
IMAP: Enable IMAP in Gmail settings for reply checking.

## Security Warning

Do not share credentials or App Passwords. Keep them secure and local.
Responsible Use: Ensure compliance with email policies and laws. Only contact recipients with permission.

## Dependencies

pandas: Excel file handling
plyer: Desktop notifications
openpyxl: Excel file support

## Install via:
pip install -r requirements.txt

tkinter is used for GUI notifications and is typically included with Python.

## License
MIT License 
