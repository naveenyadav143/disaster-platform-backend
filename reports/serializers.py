from rest_framework import serializers
from .models import UserProfile, Report

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()  # Nested serializer

    class Meta:
        model = Report
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user, created = UserProfile.objects.get_or_create(
            uid=user_data["uid"],
            defaults={
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "phone": user_data.get("phone"),
            }
        )
        return Report.objects.create(user=user, **validated_data)
