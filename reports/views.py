from rest_framework import generics
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Report, UserProfile
from .serializers import ReportSerializer
from .utils import send_push
import json
import math

@csrf_exempt
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    uid = data.get("uid")
    if not uid:
        return JsonResponse({"error": "UID required"}, status=400)

    user, created = UserProfile.objects.get_or_create(
        uid=uid,
        defaults={
            "name": data.get("name", ""),
            "email": data.get("email", ""),
            "phone": data.get("phone", ""),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }
    )

    if created:
        return JsonResponse({"message": "User created"})
    else:
        return JsonResponse({"message": "User already exists"})
# ---------------------------
# Haversine Formula (meters)
# ---------------------------
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two lat/lon in meters.
    """
    R = 6371000  # radius of Earth in meters
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


# ---------------------------
# Notify Nearby Users
# ---------------------------
def notify_nearby_users(report, radius_m=500):
    """
    Notify all users within radius_m meters of the incident location.
    """
    if not report.incidentLocation:
        return

    try:
        lat, lon = map(float, report.incidentLocation.split(","))
    except Exception:
        return  # invalid location format, skip

    users = UserProfile.objects.exclude(latitude=None).exclude(longitude=None)

    for user in users:
        distance = haversine(lat, lon, user.latitude, user.longitude)
        if distance <= radius_m and user.subscription:
            send_push(
                subscription=user.subscription,
                title=f"🚨 {report.disasterType}",
                message=f"A {report.disasterType} was reported near you ({distance:.0f} m away)."
            )


# ---------------------------
# Report Views
# ---------------------------
class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all().order_by("-timestamp")
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        report = serializer.save()
        notify_nearby_users(report)  # 🚨 trigger notification


class ReportUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_field = "reporterId"


# ---------------------------
# Subscription Management
# ---------------------------
@csrf_exempt
def save_subscription(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    uid = request.GET.get("uid")
    if not uid:
        return JsonResponse({"error": "UID not provided"}, status=400)

    try:
        user = UserProfile.objects.get(uid=uid)
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user.subscription = data
    user.save()

    return JsonResponse({"message": "Subscription saved"})

def list_subscriptions(request):
    """
    List all user subscriptions (debugging only).
    """
    data = list(UserProfile.objects.values("uid", "subscription"))
    return JsonResponse(data, safe=False)


# ---------------------------
# Test Notification Endpoint
# ---------------------------
@csrf_exempt
def test_notification(request):
    """
    Send a test notification to a single user by uid.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            uid = data.get("uid")
            title = data.get("title", "🚨 Test Alert")
            message = data.get("message", "This is a test notification.")

            user = UserProfile.objects.get(uid=uid)

            if not user.subscription:
                return JsonResponse({"error": "No subscription for this user"}, status=400)

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
