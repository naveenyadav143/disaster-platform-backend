from django.db import models

class UserProfile(models.Model):
    uid = models.CharField(max_length=100, unique=True)  # Firebase UID
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    subscription = models.JSONField(null=True, blank=True)
    def __str__(self):
        return self.name or self.email or self.uid


class Report(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reports")

    disaster_type = models.CharField(max_length=100)
    disaster_severity = models.CharField(max_length=50, null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    reporter_location = models.CharField(max_length=255, null=True, blank=True)  # "lat, long"
    incident_location = models.CharField(max_length=255, null=True, blank=True)  # "lat, long"
    location = models.CharField(max_length=255, null=True, blank=True)  # raw address/place name

    status = models.CharField(max_length=50, default="Pending")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disaster_type} by {self.user.name if self.user else 'Unknown'}"
