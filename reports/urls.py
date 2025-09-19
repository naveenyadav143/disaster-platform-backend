from django.urls import path
from .views import (
    ReportListCreateView,
    ReportUpdateView,
    save_subscription,
    list_subscriptions,
    test_notification,
    create_user,
)

urlpatterns = [
    # Report APIs
    path("reports/", ReportListCreateView.as_view(), name="report_list_create"),
    path("reports/<str:reporterId>/", ReportUpdateView.as_view(), name="report_update"),

    # Subscription APIs
    path("save-subscription/", save_subscription, name="save_subscription"),
    path("subscriptions/", list_subscriptions, name="list_subscriptions"),

    # Test Notifications
    path("test-notification/", test_notification, name="test_notification"),
    path("create-user/", create_user, name="create_user"),

]
