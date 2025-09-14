from django.db import models

class Report(models.Model):
    DISASTER_TYPES = [
        ('fire', 'Fire'),
        ('flood', 'Flood'),
        ('earthquake', 'Earthquake'),
        ('cyclone', 'Cyclone'),
        ('other', 'Other'),
    ]

    disaster_type = models.CharField(max_length=50, choices=DISASTER_TYPES)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='reports/', null=True, blank=True)
    status = models.CharField(max_length=20, default="Pending")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disaster_type} - {self.status}"
