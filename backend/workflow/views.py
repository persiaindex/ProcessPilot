from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .auth_utils import is_admin, is_reviewer
from .models import Department, Request
from .permissions import RequestPermission
from .serializers import (
    DepartmentSerializer,
    RequestSerializer,
    WorkflowActionSerializer,
)
from .services import change_request_status


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all().order_by("name")
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    permission_classes = [RequestPermission]

    def get_queryset(self):
        queryset = Request.objects.select_related(
            "department",
            "created_by",
            "assigned_reviewer",
        ).order_by("-created_at")

        user = self.request.user

        if is_admin(user):
            return queryset

        if is_reviewer(user):
            return queryset.filter(
                Q(created_by=user) | Q(assigned_reviewer=user)
            ).distinct()

        return queryset.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        request_obj = self.get_object()
        serializer = WorkflowActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_request_status(
            request_obj=request_obj,
            new_status=Request.Status.SUBMITTED,
            changed_by=request.user,
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
            changed_by=request.user,
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
            changed_by=request.user,
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
            changed_by=request.user,
            note=serializer.validated_data.get("note", ""),
        )

        return Response(
            {
                "message": "Request rejected successfully.",
                "status": Request.Status.REJECTED,
            },
            status=status.HTTP_200_OK,
        )