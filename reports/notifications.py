from pywebpush import webpush
from django.conf import settings

def send_push(subscription_info, payload):
    try:
        return webpush(
            subscription_info=subscription_info,
            data=payload,
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={"sub": settings.VAPID_EMAIL}
        )
    except Exception as e:
        print("Push failed:", e)
        return None
