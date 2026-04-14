from django.contrib import admin

from .models import Comment, Department, Request, StatusHistory


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "created_at", "updated_at")
    search_fields = ("name", "code")
    ordering = ("name",)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "priority",
        "department",
        "created_by",
        "assigned_reviewer",
        "processing_status",
        "created_at",
    )
    list_filter = ("status", "priority", "processing_status", "department")
    search_fields = ("title", "description", "created_by__username")
    autocomplete_fields = ("department", "created_by", "assigned_reviewer")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "author", "created_at")
    search_fields = ("body", "author__username", "request__title")
    autocomplete_fields = ("request", "author")
    readonly_fields = ("created_at", "updated_at")


@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "request",
        "old_status",
        "new_status",
        "changed_by",
        "changed_at",
    )
    list_filter = ("new_status", "changed_at")
    search_fields = ("request__title", "changed_by__username", "note")
    autocomplete_fields = ("request", "changed_by")
    readonly_fields = ("changed_at",)