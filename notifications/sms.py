import os
import requests
from llm.message_writer import generate_sms  # ✅ your LLM function

# Environment variables (set these once)
BULKSMS_EMAIL = os.getenv("BULKSMS_EMAIL")
BULKSMS_PASSWORD = os.getenv("BULKSMS_PASSWORD")

def send_sms(student, job1, job2):
    """
    Generate AI-based SMS and send via BulkSMSLive API.
    """
    # 1️⃣ Generate personalized SMS with your LLM
    message = generate_sms(student, job1, job2)

    # 2️⃣ (Optional) Shorten or truncate if too long
    if len(message) > 480:
        message = message[:477] + "..."

    # 3️⃣ Build request payload
    payload = {
        "email": BULKSMS_EMAIL,
        "password": BULKSMS_PASSWORD,
        "message": message,
        "sender_name": "JobAlert",
        "recipients": student["phone"],  # e.g. "2347011770092"
        "forcednd": 1  # bypass DND
    }

    # 4️⃣ Send SMS via BulkSMSLive
    try:
        response = requests.post("https://api.bulksmslive.com/v2/app/sms", data=payload)
        result = response.json()

        if result.get("status") == 1:
            print(f"✅ SMS sent to {student['name']} ({student['phone']}) | MsgID: {result['msgid']}")
        else:
            print(f"⚠️ Failed to send SMS to {student['phone']}: {result.get('msg', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error sending SMS to {student['phone']}: {e}")
