from rest_framework import serializers
from .models import UserProfile, Report

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    # Instead of full nested dict, accept just uid string
    user = serializers.SlugRelatedField(
        slug_field="uid",
        queryset=UserProfile.objects.all()
    )

    class Meta:
        model = Report
        fields = "__all__"
