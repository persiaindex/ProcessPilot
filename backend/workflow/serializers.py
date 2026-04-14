from rest_framework import serializers

from .models import Department, Request


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "code", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class RequestSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    created_by_username = serializers.CharField(
        source="created_by.username",
        read_only=True,
    )
    assigned_reviewer_username = serializers.CharField(
        source="assigned_reviewer.username",
        read_only=True,
        default=None,
    )

    class Meta:
        model = Request
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "department",
            "department_name",
            "created_by",
            "created_by_username",
            "assigned_reviewer",
            "assigned_reviewer_username",
            "ai_suggested_category",
            "processing_status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]