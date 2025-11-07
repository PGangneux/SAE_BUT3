from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Nation
from ...tests import Neo4jTestCase


class NationViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        self.nation1 = Nation(name=f"Nation_{uuid4()}").save()
        self.nation2 = Nation(name=f"Nation_{uuid4()}").save()

    def test_list_nations(self):
        url = reverse('nation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(n['uuid'] == self.nation1.uuid for n in response.json()))
        self.assertTrue(any(n['uuid'] == self.nation2.uuid for n in response.json()))

    def test_retrieve_nation(self):
        url = reverse('nation-detail', kwargs={'uuid': self.nation1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['uuid'], self.nation1.uuid)

    def test_retrieve_nonexistent_nation(self):
        url = reverse('nation-detail', kwargs={'uuid': '00000000-0000-0000-0000-000000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
