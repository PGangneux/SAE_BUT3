from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import StyleMusical
from ...tests import Neo4jTestCase


class StyleMusicalViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        self.style1 = StyleMusical(name=f"Style_{uuid4()}").save()
        self.style2 = StyleMusical(name=f"Style_{uuid4()}").save()

    def test_list_styles(self):
        """
        Vérifie que la liste des styles musicaux est correctement renvoyée
        """
        url = reverse("style-musical-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertTrue(any(s["uuid"] == self.style1.uuid for s in data))
        self.assertTrue(any(s["uuid"] == self.style2.uuid for s in data))

    def test_retrieve_style(self):
        """
        Vérifie qu'un style musical peut être récupéré individuellement
        """
        url = reverse("style-musical-detail", kwargs={"uuid": self.style1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.style1.uuid)

    def test_retrieve_nonexistent_style(self):
        """
        Vérifie qu'une requête sur un style musical inexistant renvoie 404
        """
        url = reverse(
            "style-musical-detail",
            kwargs={"uuid": "00000000-0000-0000-0000-000000000000"},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
