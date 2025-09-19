from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Report

class ReportUpdateTestCase(APITestCase):
    def setUp(self):
        self.report = Report.objects.create(
            reporterId='test_reporter_123',
            disasterType='Flood',
            status='Pending'
        )

    def test_put_update_report_status(self):
        url = reverse('report-update', kwargs={'reporterId': self.report.reporterId})
        data = {
            'reporterId': self.report.reporterId,
            'disasterType': 'Flood',
            'status': 'Resolved'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, 'Resolved')
