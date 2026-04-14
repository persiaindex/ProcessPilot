from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DepartmentViewSet, RequestViewSet

router = DefaultRouter()
router.register("departments", DepartmentViewSet, basename="department")
router.register("requests", RequestViewSet, basename="request")

urlpatterns = [
    path("", include(router.urls)),
]