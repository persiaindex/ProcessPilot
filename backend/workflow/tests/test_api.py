from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from workflow.models import Department, Request


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.employee_group, _ = Group.objects.get_or_create(name="employee")
        self.reviewer_group, _ = Group.objects.get_or_create(name="reviewer")
        self.admin_group, _ = Group.objects.get_or_create(name="admin")

        self.employee1 = User.objects.create_user(
            username="employee1",
            password="employee1pass",
            email="employee1@example.com",
        )
        self.employee2 = User.objects.create_user(
            username="employee2",
            password="employee2pass",
            email="employee2@example.com",
        )
        self.reviewer1 = User.objects.create_user(
            username="reviewer1",
            password="reviewer1pass",
            email="reviewer1@example.com",
        )
        self.admin1 = User.objects.create_user(
            username="admin1",
            password="admin1pass",
            email="admin1@example.com",
            is_staff=True,
        )

        self.employee1.groups.add(self.employee_group)
        self.employee2.groups.add(self.employee_group)
        self.reviewer1.groups.add(self.reviewer_group)
        self.admin1.groups.add(self.admin_group)

        self.employee1_token = Token.objects.create(user=self.employee1)
        self.employee2_token = Token.objects.create(user=self.employee2)
        self.reviewer1_token = Token.objects.create(user=self.reviewer1)
        self.admin1_token = Token.objects.create(user=self.admin1)

        self.department = Department.objects.create(
            name="Engineering",
            code="ENG",
        )

        self.request_obj = Request.objects.create(
            title="Simulation workstation upgrade",
            description="Current workstation is too slow for physics simulations.",
            priority="high",
            department=self.department,
            created_by=self.employee1,
            assigned_reviewer=self.reviewer1,
        )

    def authenticate(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def clear_auth(self):
        self.client.credentials()


class AuthApiTests(BaseAPITestCase):
    def test_login_returns_token_and_user_payload(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "employee1",
                "password": "employee1pass",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], "employee1")
        self.assertEqual(response.data["user"]["role"], "employee")

    def test_me_endpoint_returns_current_user(self):
        self.authenticate(self.employee1_token)

        response = self.client.get("/api/auth/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "employee1")
        self.assertEqual(response.data["role"], "employee")


class RequestCreationTests(BaseAPITestCase):
    def test_authenticated_user_can_create_request_and_created_by_is_automatic(self):
        self.authenticate(self.employee1_token)

        response = self.client.post(
            "/api/requests/",
            {
                "title": "Need a faster laptop",
                "description": "Rendering and simulation tasks are too slow.",
                "priority": "medium",
                "department": self.department.id,
                "assigned_reviewer": self.reviewer1.id,
                "created_by": self.employee2.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_request = Request.objects.get(id=response.data["id"])
        self.assertEqual(created_request.created_by, self.employee1)
        self.assertEqual(created_request.assigned_reviewer, self.reviewer1)


class RequestVisibilityPermissionTests(BaseAPITestCase):
    def test_employee_only_sees_own_requests(self):
        other_request = Request.objects.create(
            title="Office chair replacement",
            description="The chair is broken.",
            priority="low",
            department=self.department,
            created_by=self.employee2,
            assigned_reviewer=self.reviewer1,
        )

        self.authenticate(self.employee1_token)
        response = self.client.get("/api/requests/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = [item["id"] for item in response.data]
        self.assertIn(self.request_obj.id, returned_ids)
        self.assertNotIn(other_request.id, returned_ids)

    def test_reviewer_can_see_assigned_request(self):
        self.authenticate(self.reviewer1_token)
        response = self.client.get("/api/requests/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = [item["id"] for item in response.data]
        self.assertIn(self.request_obj.id, returned_ids)

    def test_unauthenticated_user_gets_auth_error_for_request_list(self):
        self.clear_auth()
        response = self.client.get("/api/requests/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_employee_cannot_approve_request_assigned_to_someone_else(self):
        self.request_obj.status = Request.Status.SUBMITTED
        self.request_obj.save(update_fields=["status", "updated_at"])

        self.authenticate(self.employee2_token)
        response = self.client.post(
            f"/api/requests/{self.request_obj.id}/approve/",
            {"note": "Trying to approve without permission."},
            format="json",
        )

        self.assertIn(
            response.status_code,
            [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND],
        )


class WorkflowTransitionTests(BaseAPITestCase):
    def test_creator_can_submit_request(self):
        self.authenticate(self.employee1_token)

        response = self.client.post(
            f"/api/requests/{self.request_obj.id}/submit/",
            {"note": "Ready for review."},
            format="json",
        )

        self.request_obj.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.request_obj.status, Request.Status.SUBMITTED)

    def test_assigned_reviewer_can_start_review_and_approve(self):
        self.request_obj.status = Request.Status.SUBMITTED
        self.request_obj.save(update_fields=["status", "updated_at"])

        self.authenticate(self.reviewer1_token)

        start_review_response = self.client.post(
            f"/api/requests/{self.request_obj.id}/start_review/",
            {"note": "Starting the review."},
            format="json",
        )
        self.request_obj.refresh_from_db()
        self.assertEqual(start_review_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.request_obj.status, Request.Status.IN_REVIEW)

        approve_response = self.client.post(
            f"/api/requests/{self.request_obj.id}/approve/",
            {"note": "Approved after validation."},
            format="json",
        )
        self.request_obj.refresh_from_db()
        self.assertEqual(approve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.request_obj.status, Request.Status.APPROVED)

    def test_invalid_transition_returns_400(self):
        self.authenticate(self.reviewer1_token)

        response = self.client.post(
            f"/api/requests/{self.request_obj.id}/approve/",
            {"note": "Trying to skip required steps."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)