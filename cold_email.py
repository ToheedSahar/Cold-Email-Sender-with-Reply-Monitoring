import pandas as pd
import time
import random
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header
import sqlite3
import datetime
import threading
import tkinter as tk
from tkinter import messagebox
import logging
from plyer import notification

# Set up logging
logging.basicConfig(filename='email_script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# SQLite database setup
conn = sqlite3.connect('email_log.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sent_emails
             (email TEXT, channel_name TEXT, sent_time REAL, follow_up_sent INTEGER)''')
conn.commit()

# Email sending function
def send_email(to_email, channel_name, follow_up=False):
    from_email = "programmertoheedsahar@gmail.com"  # Replace with your Gmail
    app_password = "***************"   # Replace with your Gmail App Password

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email

    if not follow_up:
        msg['Subject'] = "Struggling with File Conversion? Let Me Handle It for You"
        html = f"""
        <html>
        <body>
        <p>Greeting,</p>
        <p>I know how frustrating file conversion can be—whether you're an author finalizing an eBook, a publisher ensuring flawless formatting, or a researcher needing structured data. A single conversion issue can derail your entire workflow:</p>
        <ul>
        <li>🚨 Lost Formatting – Broken layouts, missing fonts, or alignment issues</li>
        <li>🚨 Non-Clickable Table of Contents – A nightmare for eBook navigation</li>
        <li>🚨 Messed-up Data Extraction – Tables and numbers losing structure in Excel</li>
        <li>🚨 ePub & Mobi Glitches – Inconsistent layouts across Kindle and other devices</li>
        <li>🚨 Scanned PDFs with OCR Errors – Garbled text that’s impossible to edit</li>
        </ul>
        <p>These problems waste hours of your time—time better spent on writing, editing, and publishing.</p>
        <h3><b>Why Work With Me?</b></h3>
        <p>I don’t just rely on basic conversion tools—I’m a <i>Python programmer</i> who has built custom tools to increase conversion accuracy beyond standard software capabilities. Plus, I use premium tools like Adobe Acrobat Pro, ABBYY FineReader, and Kindle Previewer to ensure precision.</p>
        <h3><b>Services I Offer</b></h3>
        <ul>
        <li>✅ PDF to Word/ePub/Mobi – Perfect structure & formatting retained</li>
        <li>✅ Word to ePub/Mobi – Ready-to-publish files, clickable TOCs included</li>
        <li>✅ Excel Data Extraction – Clean, structured data without loss</li>
        <li>✅ Advanced OCR for Scanned PDFs – Editable text, no garbled characters</li>
        <li>✅ Bulk Conversions & Custom Formatting – Fast delivery without errors</li>
        </ul>
        <p><b>Your File, Your Format – Just Send It Over</b></p>
        <p>Simply attach your files and let me handle the tedious work for you. I’ll ensure 100% accuracy, proper structure, and industry-standard formatting—so you don’t have to worry about technical headaches.</p>
        <p>Let’s discuss how I can help streamline your workflow! Just reply to this email, and we’ll get started.</p>
        <p>Looking forward to working with you,</p>
        <p>Toheed Sahar<br>programmertoheedsahar@gmail.com</p>
        </body>
        </html>
        """
    else:
        msg['Subject'] = "Let's Perfect Your Document Conversions"
        html = f"""
        <html>
        <body>
        <p>Greeting,</p>
        <p>Just Imagine: This could be the step that transforms your document workflow and boosts your business efficiency. Let's make those conversion challenges a thing of the past!</p>
        <p>I'm here ready to help you with:</p>
        <ul>
        <li>Same-day turnaround for urgent projects</li>
        <li>Custom formatting solutions</li>
        <li>Bulk processing discounts</li>
        <li>100% accuracy guarantee</li>
        </ul>
        <p>Take the next step in streamlining your operations. Just reply with your files and requirements.</p>
        <p>Best regards,<br>Toheed Sahar</p>
        </body>
        </html>
        """

    part = MIMEText(html, 'html')
    msg.attach(part)

    for attempt in range(3):  # Retry mechanism
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(from_email, app_password)
                server.sendmail(from_email, to_email, msg.as_string())
            logging.info(f"Sent {'follow-up ' if follow_up else ''}email to {to_email}")
            return True
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed to send email to {to_email}: {e}")
            time.sleep(5)  # Wait before retrying
    return False

# Function to check for replies
def check_reply(from_email, sent_time):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login("your_email@gmail.com", "your_app_password")
        mail.select("inbox")
        result, data = mail.search(None, f'(FROM "{from_email}" SINCE "{sent_time.strftime("%d-%b-%Y")}")')
        mail.close()
        mail.logout()
        return result == 'OK' and data[0]
    except Exception as e:
        logging.error(f"Error checking reply from {from_email}: {e}")
        return False

# Function to get reply details
def get_new_replies(from_email, sent_time):
    replies = []
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login("your_email@gmail.com", "your_app_password")
        mail.select("inbox")
        result, data = mail.search(None, f'(FROM "{from_email}" SINCE "{sent_time.strftime("%d-%b-%Y")}")')
        if result == 'OK':
            for num in data[0].split():
                result, msg_data = mail.fetch(num, '(RFC822)')
                if result == 'OK':
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    date_tuple = email.utils.parsedate_tz(msg['Date'])
                    if date_tuple:
                        email_time = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                        if email_time > sent_time:
                            body = get_email_body(msg)
                            replies.append({'time': email_time, 'body': body, 'serial': num.decode()})
        mail.close()
        mail.logout()
    except Exception as e:
        logging.error(f"Error fetching replies from {from_email}: {e}")
    return replies

# Extract email body
def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(errors='ignore')
    return msg.get_payload(decode=True).decode(errors='ignore')

# GUI notification for replies
def show_reply_notification(email, reply_time, body, serial):
    def read_more():
        full_window = tk.Toplevel(root)
        full_window.title(f"Reply from {email}")
        tk.Label(full_window, text=f"S.L: {serial}\nSender: {email}\nReceiver: your_email@gmail.com\nTime: {reply_time}\n\n{body}", wraplength=400, justify="left").pack(padx=10, pady=10)
        tk.Button(full_window, text="Close", command=full_window.destroy).pack(pady=5)

    root = tk.Tk()
    root.withdraw()  # Hide main window
    notification.notify(title=f"New Reply from {email}", message=f"At {reply_time}: {body[:100]}...", timeout=10)
    messagebox.showinfo("New Reply", f"S.L: {serial}\nSender: {email}\nReceiver: your_email@gmail.com\nTime: {reply_time}\n\n{body[:100]}...",
                        detail="Click OK to read more or close.", parent=root)
    read_more_btn = messagebox.askyesno("Read More?", "Would you like to read the full email?", parent=root)
    if read_more_btn:
        read_more()
    root.destroy()

# Send initial emails
def send_initial_emails():
    df = pd.read_excel("emails.xlsx")
    for index, row in df.iterrows():
        if pd.notna(row['Gmail']) and row['Gmail'] != '-':
            email = row['Gmail']
            channel_name = row['Name']
            c.execute("SELECT * FROM sent_emails WHERE email = ?", (email,))
            if not c.fetchone():  # Only send if not already sent
                if send_email(email, channel_name):
                    c.execute("INSERT INTO sent_emails VALUES (?, ?, ?, 0)", (email, channel_name, time.time()))
                    conn.commit()
                delay = random.randint(5760, 5850)  # adjust delay in sec.
                time.sleep(delay)

# Check replies and send follow-ups
def monitor_replies():
    while True:
        c.execute("SELECT * FROM sent_emails")
        for row in c.fetchall():
            email, channel_name, sent_time, follow_up_sent = row
            sent_time_dt = datetime.datetime.fromtimestamp(sent_time)
            current_time = datetime.datetime.now()

            # Check for replies
            replies = get_new_replies(email, sent_time_dt)
            for reply in replies:
                show_reply_notification(email, reply['time'], reply['body'], reply['serial'])

            # Send follow-up if 60 hours passed and no reply
            if current_time - sent_time_dt > datetime.timedelta(hours=60) and not follow_up_sent:
                if not check_reply(email, sent_time_dt):
                    if send_email(email, channel_name, follow_up=True):
                        c.execute("UPDATE sent_emails SET follow_up_sent = 1 WHERE email = ?", (email,))
                        conn.commit()
        time.sleep(3600)  # Check every hour

# Main execution
if __name__ == "__main__":
    # Start initial email sending in a separate thread
    threading.Thread(target=send_initial_emails, daemon=True).start()
    # Start reply monitoring in the main thread
    monitor_replies()
