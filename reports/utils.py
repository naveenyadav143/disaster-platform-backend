from pywebpush import webpush, WebPushException
import json

def send_push(subscription, title, message):
    try:
        webpush(
            subscription_info=subscription,
            data=json.dumps({"title": title, "message": message}),
            vapid_private_key="YOUR_VAPID_PRIVATE_KEY",
            vapid_claims={"sub": "mailto:you@example.com"},
        )
        print("Push sent successfully ✅")
    except WebPushException as e:
        print("Push failed ❌", e)

def send_notification(report):
    """
    Send a push notification for a new report.
    """
    user = report.user
    if user and user.subscription:
        title = f"New {report.disaster_type} Report"
        message = report.description or "A new disaster report has been submitted."
        send_push(user.subscription, title, message)
