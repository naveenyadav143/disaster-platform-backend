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
# Update Report (status) and Delete
class ReportUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_field = 'reporterId'

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
from django.http import JsonResponse
from .models import UserProfile

def list_subscriptions(request):
    data = list(UserProfile.objects.values("uid", "subscription"))
    return JsonResponse(data, safe=False)


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
    if not report.incidentLocation:
        return

    lat, lon = map(float, report.incidentLocation.split(","))
    users = UserProfile.objects.exclude(latitude=None).exclude(longitude=None)

    for user in users:
        distance = haversine(lat, lon, user.latitude, user.longitude)
        if distance <= radius_km and user.subscription:
            send_push(
                subscription=user.subscription,
                title=f"🚨 {report.disasterType}",
                message=f"A {report.disasterType} was reported near you ({distance:.1f} km away)."
            )
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import UserProfile
from .utils import send_push

@csrf_exempt
def test_notification(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            uid = data.get("uid")
            title = data.get("title", "🚨 Test Alert")
            message = data.get("message", "This is a test notification.")

            # Find the user
            user = UserProfile.objects.get(uid=uid)

            if not user.subscription:
                return JsonResponse({"error": "No subscription for this user"}, status=400)

            # Send push notification
            send_push(
                subscription=user.subscription,
                title=title,
                message=message
            )

            return JsonResponse({"message": "Notification sent!"})
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)
