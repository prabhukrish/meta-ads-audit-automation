import os
import requests
from dotenv import load_dotenv
from datetime import date

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("ALERT_EMAIL_FROM")
RECEIVER_EMAILS = os.getenv("ALERT_EMAIL_TO", "").split(",")

if not BREVO_API_KEY or not SENDER_EMAIL or not RECEIVER_EMAILS:
    raise RuntimeError("Email environment variables are not set")

def send_email_alert(ad):
    url = "https://api.brevo.com/v3/smtp/email"
    print("🔥 send_email_alert triggered")
    # ✅ Print separately (correct way)

    payload = {
        "sender": {
            "email": SENDER_EMAIL,
            "name": "Creative Fatigue Alert"
        },
        "to": [
            {"email": email.strip()} for email in RECEIVER_EMAILS if email.strip()
        ],
        "subject": "🚨 Creative Fatigue Detected",
        "htmlContent": f"""
        <h2>Creative Fatigue Alert</h2>
        <p><strong>Ad Name:</strong> {ad['ad_name']}</p>
        <p>This creative has triggered fatigue rules.</p>
        """
    }

    headers = {
        "Accept": "application/json",
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        print("📧 Email alert sent successfully")
    else:
        print("❌ Email alert failed")
        print(response.status_code, response.text)

def send_daily_audit_email(html_content):
    from datetime import date
    subject_date = date.today().strftime("%d %b %Y")

    
    payload = {
        "sender": {"email": SENDER_EMAIL},
        "to": [{"email": email.strip()} for email in RECEIVER_EMAILS],
        "subject": f"📊 Meta Ads Daily Audit – {subject_date}",
        "htmlContent": html_content,
    }

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        json=payload,
        headers={
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
        },
    )
    print("📧 Brevo status:", response.status_code)
    print("📧 Brevo response:", response.text)
    
    response.raise_for_status()
