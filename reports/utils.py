from pywebpush import webpush, WebPushException
from decouple import config
import json

# Load keys from .env file
VAPID_PRIVATE_KEY = config("VAPID_PRIVATE_KEY")
VAPID_PUBLIC_KEY = config("VAPID_PUBLIC_KEY")
VAPID_EMAIL = config("VAPID_EMAIL")  # e.g. mailto:balaganinaveenyd@gmail.com


def send_push(subscription, title, message):
    try:
        webpush(
            subscription_info=subscription,
            data=json.dumps({"title": title, "message": message}),
            vapid_private_key=VAPID_PRIVATE_KEY,   # ✅ actual private key
            vapid_claims={"sub": VAPID_EMAIL},
        )
        print("Push sent successfully ✅")
        return {"status": "success"}
    except WebPushException as e:
        print("Push failed ❌", e)
        return {"status": "failed", "details": str(e)}


from .models import UserProfile

def send_notification(report):
    """
    Send a push notification for a new report.
    """
    user = None
    if report.reporterId:
        try:
            user = UserProfile.objects.get(uid=report.reporterId)
        except UserProfile.DoesNotExist:
            user = None

    if user and user.subscription:
        title = f"New {report.disasterType} Report"
        message = report.description or "A new disaster report has been submitted."
        send_push(user.subscription, title, message)
