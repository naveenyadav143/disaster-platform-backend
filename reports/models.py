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
    reporterId = models.CharField(max_length=100, default="")  # currentUser.uid
    reporterEmail = models.EmailField(null=True, blank=True)  # currentUser.email
    reporterName = models.CharField(max_length=100, null=True, blank=True)  # form.reporterName
    reporterPhone = models.CharField(max_length=15, null=True, blank=True)  # form.phone

    disasterType = models.CharField(max_length=100)  # disasterTypeToSend
    disasterSeverity = models.CharField(max_length=50, null=True, blank=True)  # form.severity

    description = models.TextField(null=True, blank=True)  # form.description
    imageUrl = models.URLField(null=True, blank=True)  # imgURL

    reporterLocation = models.CharField(max_length=255, null=True, blank=True)  # locationData.currentLocation.join(", ")
    incidentLocation = models.CharField(max_length=255, null=True, blank=True)  # locationData.selectedLocation.join(", ")
    location = models.CharField(max_length=255, null=True, blank=True)  # form.location (IncidentLocation)
    accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="Pending")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disasterType} by {self.reporterName or 'Unknown'}"
