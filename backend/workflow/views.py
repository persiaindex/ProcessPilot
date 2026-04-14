from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Department, Request
from .serializers import (
    DepartmentSerializer,
    RequestSerializer,
    WorkflowActionSerializer,
)
from .services import change_request_status


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

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        request_obj = self.get_object()
        serializer = WorkflowActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_request_status(
            request_obj=request_obj,
            new_status=Request.Status.SUBMITTED,
            changed_by=request.user if request.user.is_authenticated else None,
            note=serializer.validated_data.get("note", ""),
        )

        return Response(
            {
                "message": "Request submitted successfully.",
                "status": Request.Status.SUBMITTED,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def start_review(self, request, pk=None):
        request_obj = self.get_object()
        serializer = WorkflowActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_request_status(
            request_obj=request_obj,
            new_status=Request.Status.IN_REVIEW,
            changed_by=request.user if request.user.is_authenticated else None,
            note=serializer.validated_data.get("note", ""),
        )

        return Response(
            {
                "message": "Request moved to in_review successfully.",
                "status": Request.Status.IN_REVIEW,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        request_obj = self.get_object()
        serializer = WorkflowActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_request_status(
            request_obj=request_obj,
            new_status=Request.Status.APPROVED,
            changed_by=request.user if request.user.is_authenticated else None,
            note=serializer.validated_data.get("note", ""),
        )

        return Response(
            {
                "message": "Request approved successfully.",
                "status": Request.Status.APPROVED,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        request_obj = self.get_object()
        serializer = WorkflowActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_request_status(
            request_obj=request_obj,
            new_status=Request.Status.REJECTED,
            changed_by=request.user if request.user.is_authenticated else None,
            note=serializer.validated_data.get("note", ""),
        )

        return Response(
            {
                "message": "Request rejected successfully.",
                "status": Request.Status.REJECTED,
            },
            status=status.HTTP_200_OK,
        )