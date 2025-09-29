from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theater.models import Actor


class ActorAdminTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse("theater:actor-list")
        self.actor = Actor.objects.create(first_name="Tom", last_name="Hanks")
        self.retrieve_url = reverse("theater:actor-detail", args=[self.actor.id])
        self.user = get_user_model().objects.create_superuser(
            "admin@admin.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_list_actor(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("first_name", response.data[0])

    def test_retrieve_actor(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Tom")
        self.assertEqual(response.data["full_name"], "Tom Hanks")

    def test_create_actor(self):
        data = {"first_name": "John", "last_name": "Doe"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Actor.objects.filter(first_name="John").exists())


class ActorUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("user@user.com", "password")
        self.client.force_authenticate(self.user)
        self.actor = Actor.objects.create(first_name="Tom", last_name="Hanks")
        self.list_url = reverse("theater:actor-list")
        self.retrieve_url = reverse("theater:actor-detail", args=[self.actor.id])

    def test_list_actor(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("first_name", response.data[0])

    def test_retrieve_actor(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Tom")
        self.assertEqual(response.data["full_name"], "Tom Hanks")

    def test_create_actor(self):
        data = {"first_name": "John", "last_name": "Doe"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(not Actor.objects.filter(first_name="John").exists())
