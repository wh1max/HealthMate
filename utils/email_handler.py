
from flask_mail import Message

def send_email(mail, recipient, symptoms, summary):
    """
    Sends the health summary email to the user.
    """
    msg = Message(
        subject="Your HealthMate AI Summary",
        recipients=[recipient],
        body=f"""
Hello,

Thank you for using HealthMate AI.

Here is the health summary based on the information you provided.

Original Symptoms: {symptoms}

AI-Generated Summary:
{summary}

---
**Disclaimer:** This is not a medical diagnosis. This tool is for informational purposes only and does not replace professional medical advice. Please consult with a qualified healthcare provider for any health concerns.
        """
    )
    mail.send(msg)
