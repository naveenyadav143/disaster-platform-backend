# reports/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Report
from .utils import send_notification  # your notification function

@receiver(post_save, sender=Report)
def report_created_notify(sender, instance, created, **kwargs):
    if created:
        # Automatically send notification when a new report is created
        send_notification(instance)
