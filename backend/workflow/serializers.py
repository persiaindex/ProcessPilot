from rest_framework import serializers

from .models import Department, Request


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "code", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class RequestSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    created_by_username = serializers.SerializerMethodField()
    assigned_reviewer_username = serializers.SerializerMethodField()

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
        read_only_fields = [
            "id",
            "status",
            "ai_suggested_category",
            "processing_status",
            "created_at",
            "updated_at",
        ]

    def get_department_name(self, obj):
        return obj.department.name

    def get_created_by_username(self, obj):
        return obj.created_by.username

    def get_assigned_reviewer_username(self, obj):
        if obj.assigned_reviewer is None:
            return None
        return obj.assigned_reviewer.username

    def validate(self, attrs):
        instance = getattr(self, "instance", None)

        if instance and instance.status in {
            Request.Status.APPROVED,
            Request.Status.REJECTED,
        }:
            blocked_fields = {
                "title",
                "description",
                "priority",
                "department",
                "assigned_reviewer",
            }
            attempted_updates = blocked_fields.intersection(attrs.keys())
            if attempted_updates:
                raise serializers.ValidationError(
                    "Approved or rejected requests can no longer be edited."
                )

        return attrs


class WorkflowActionSerializer(serializers.Serializer):
    note = serializers.CharField(required=False, allow_blank=True)