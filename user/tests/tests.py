# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
#
#
# class UserTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_superuser(
#             "admin@admin.com", "password"
#         )
#         self.client.force_authenticate(self.user)
#
#     def test_create_account(self):
#         url = reverse("user:users-list")
#         data = {"name": "User"}
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
