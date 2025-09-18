from rest_framework import generics
from .models import Report
from .serializers import ReportSerializer
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserProfile

# Create Report & List All
class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all().order_by('-timestamp')
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        report = serializer.save()
        notify_nearby_users(report)  # 🚨
# Update Report (status)
class ReportUpdateView(generics.UpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

@csrf_exempt
def save_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = request.GET.get("uid")  # Firebase UID

        user = UserProfile.objects.get(uid=uid)
        user.subscription = data
        user.save()

        return JsonResponse({"message": "Subscription saved"})

from django.db.models import Q
from .models import UserProfile
from .utils import send_push
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2) ** 2)
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def notify_nearby_users(report, radius_km=5):
    if not report.incident_location:
        return
    
    lat, lon = map(float, report.incident_location.split(","))
    users = UserProfile.objects.exclude(latitude=None).exclude(longitude=None)

    for user in users:
        distance = haversine(lat, lon, user.latitude, user.longitude)
        if distance <= radius_km and user.subscription:
            send_push(
                subscription=user.subscription,
                title=f"🚨 {report.disaster_type}",
                message=f"A {report.disaster_type} was reported near you ({distance:.1f} km away)."
            )
