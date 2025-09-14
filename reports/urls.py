from django.urls import path
from .views import ReportListCreateView, ReportUpdateView

urlpatterns = [
    path('reports/', ReportListCreateView.as_view(), name="report-list-create"),
    path('reports/<int:pk>/', ReportUpdateView.as_view(), name="report-update"),
]
