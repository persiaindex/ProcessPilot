from rest_framework.exceptions import ValidationError

from .models import Request, StatusHistory


ALLOWED_TRANSITIONS = {
    Request.Status.DRAFT: {Request.Status.SUBMITTED},
    Request.Status.SUBMITTED: {
        Request.Status.IN_REVIEW,
        Request.Status.APPROVED,
        Request.Status.REJECTED,
    },
    Request.Status.IN_REVIEW: {
        Request.Status.APPROVED,
        Request.Status.REJECTED,
    },
    Request.Status.APPROVED: set(),
    Request.Status.REJECTED: set(),
}


def change_request_status(request_obj, new_status, changed_by=None, note=""):
    old_status = request_obj.status
    allowed_next_statuses = ALLOWED_TRANSITIONS.get(old_status, set())

    if new_status not in allowed_next_statuses:
        raise ValidationError(
            {
                "status": (
                    f"Cannot change status from '{old_status}' to '{new_status}'."
                )
            }
        )

    request_obj.status = new_status
    request_obj.save(update_fields=["status", "updated_at"])

    StatusHistory.objects.create(
        request=request_obj,
        old_status=old_status,
        new_status=new_status,
        changed_by=changed_by,
        note=note,
    )

    return request_obj