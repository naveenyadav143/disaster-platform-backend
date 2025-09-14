from rest_framework import generics
from .models import Report
from .serializers import ReportSerializer

# Create Report & List All
class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all().order_by('-timestamp')
    serializer_class = ReportSerializer

# Update Report (status)
class ReportUpdateView(generics.UpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
