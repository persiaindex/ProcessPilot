from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Department, Request
from .serializers import DepartmentSerializer, RequestSerializer


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all().order_by("name")
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Request.objects.select_related(
                "department",
                "created_by",
                "assigned_reviewer",
            )
            .all()
            .order_by("-created_at")
        )