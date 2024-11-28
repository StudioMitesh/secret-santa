import smtplib
from email.mime.text import MIMEText
from random import shuffle
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

def secret_santa(participants):
    names = list(participants.keys())
    shuffle(names)

    assignments = {}
    for i in range(len(names)):
        giver = names[i]
        receiver = names[(i + 1) % len(names)]
        assignments[giver] = receiver
    return assignments

if __name__ == "__main__":
    num = int(input("Enter the number of participants: "))
    participants = {}
    for i in range(num):
        name = input(f"Enter the name of participant {i + 1}: ")
        email = input(f"Enter the email of participant {i + 1}: ")
        participants[name] = email

    sender_email = EMAIL # Use a separate email for sending emails
    sender_password = "your_email_password" # Make sure no 2FA is enabled

    assignments = secret_santa(participants)

    for giver, receiver in assignments.items():
        subject = "Your Secret Santa Assignment!"
        body = f"Hi {giver},\n\nYou are the Secret Santa for: {receiver}.\n\nHappy gifting!"
        send_email(sender_email, sender_password, participants[giver], subject, body)
