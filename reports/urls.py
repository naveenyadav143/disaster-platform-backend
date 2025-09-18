from django.urls import path
from .views import ReportListCreateView, ReportUpdateView, save_subscription,list_subscriptions

urlpatterns = [
    path('reports/', ReportListCreateView.as_view(), name="report-list-create"),
    path('reports/<int:pk>/', ReportUpdateView.as_view(), name="report-update"),
    path("save-subscription/", save_subscription, name="save_subscription"),
    path("subscriptions/", list_subscriptions, name="list_subscriptions"),  # 
]
