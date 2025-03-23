import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import sys

# Force unbuffered output to ensure messages are printed immediately
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Load environment variables for email credentials
print("Loading environment variables...")
load_dotenv()
print("Environment variables loaded")

def send_health_alert(category, patient_name, data_metric, patient_email, practitioner_email):
    from_email = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")

    if not from_email or not email_password:
        raise ValueError("EMAIL_ADDRESS and EMAIL_PASSWORD must be set in the .env file")

    category = category.lower()

    if category == "normal":
        return

    msg = EmailMessage()
    msg['From'] = from_email
    msg['To'] = practitioner_email if category == "emergency" else patient_email

    subject = "Health Alert: " + ("Emergency" if category == "emergency" else "Abnormal")
    msg['Subject'] = subject

    body = f"""
        Dear {patient_name},

        We have detected the following health issues:
        - {data_metric}

        Please take appropriate action immediately.

        ➡️ View full details: <a href="http://localhost:5173/alerts" target="_blank">View Details</a>

        Best regards,  
        Health Monitoring Team
        """

    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, email_password)
            smtp.send_message(msg)

        print(f"✅ Email sent successfully to {msg['To']}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
