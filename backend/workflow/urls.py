from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .auth_views import LoginView, LogoutView, MeView
from .views import DepartmentViewSet, RequestViewSet

router = DefaultRouter()
router.register("departments", DepartmentViewSet, basename="department")
router.register("requests", RequestViewSet, basename="request")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
]