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
