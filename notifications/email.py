import os
import re

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from llm.message_writer import generate_email


GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def html_to_text(html):
    """Quickly strip tags to make a plain text version."""
    text = re.sub(r"<[^>]+>", "", html)
    return text.strip()

def send_email(student, job1, job2):
    # Generate email body (HTML from LLM)
    email_html = generate_email(student, job1, job2)

    # Clean footer
    footer_html = """
    <hr style="border:none;border-top:1px solid #ddd;">
    <small style="color:#666;font-size:12px;">
      You are receiving this email because you subscribed to JobAlert.
      <a href="https://yourdomain.com/unsubscribe">Unsubscribe</a>
    </small>
    """

    full_html = f"""
    <html>
      <body style="font-family:Arial,sans-serif; line-height:1.6; color:#333;">
        {email_html}
        {footer_html}
      </body>
    </html>
    """

    # Also create plain text version for fallback
    full_text = html_to_text(email_html + "\n\nYou are receiving this email because you subscribed to JobAlert. Unsubscribe here: https://yourdomain.com/unsubscribe")

    # Build email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "New Job Opportunities for You"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = student['email']

    # Attach plain text and HTML parts
    msg.attach(MIMEText(full_text, "plain"))
    msg.attach(MIMEText(full_html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, student['email'], msg.as_string())
        print(f"✅ Email sent to {student['email']}")
    except Exception as e:
        print(f"❌ Error sending email to {student['email']}: {e}")
