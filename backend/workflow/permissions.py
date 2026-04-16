from rest_framework.permissions import SAFE_METHODS, BasePermission

from .auth_utils import is_admin


class RequestPermission(BasePermission):
    message = "You do not have permission to perform this action on this request."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user

        if is_admin(user):
            return True

        if request.method in SAFE_METHODS:
            return obj.created_by_id == user.id or obj.assigned_reviewer_id == user.id

        if view.action in {"update", "partial_update", "destroy", "submit"}:
            return obj.created_by_id == user.id

        if view.action in {"start_review", "approve", "reject"}:
            return obj.assigned_reviewer_id == user.id

        return False