from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Artiste, StyleMusical
from ...tests import Neo4jTestCase

class ArtisteStyleRelationShipViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Création d'un artiste
        self.artiste = Artiste(name=f"Artiste_{uuid4()}", info="info").save()
        
        # Création de deux styles
        self.style1 = StyleMusical(name=f"Style_{uuid4()}").save()
        self.style2 = StyleMusical(name=f"Style_{uuid4()}").save()
        
        # Connecter seulement style1
        self.artiste.style.connect(self.style1)

    def test_list_styles_of_artiste(self):
        url = reverse('style-list', kwargs={'artiste_uuid': self.artiste.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [s['uuid'] for s in response.json()]
        self.assertIn(self.style1.uuid, uuids)
        self.assertNotIn(self.style2.uuid, uuids)

    def test_retrieve_style_of_artiste(self):
        url = reverse('style-detail', kwargs={
            'artiste_uuid': self.artiste.uuid,
            'uuid': self.style1.uuid
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['uuid'], self.style1.uuid)

    def test_retrieve_nonexistent_style_raises_notfound(self):
        url = reverse('style-detail', kwargs={
            'artiste_uuid': self.artiste.uuid,
            'uuid': self.style2.uuid  # non connecté
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_artiste_not_found_raises_notfound(self):
        url = reverse('style-list', kwargs={'artiste_uuid': str(uuid4())})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_style_relation(self):
        url = reverse('style-list', kwargs={'artiste_uuid': self.artiste.uuid})
        payload = {'uuid': self.style2.uuid}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifie que la relation a été créée
        self.assertTrue(self.artiste.style.is_connected(self.style2))

    def test_destroy_style_relation(self):
        url = reverse('style-detail', kwargs={
            'artiste_uuid': self.artiste.uuid,
            'uuid': self.style1.uuid
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Vérifie que la relation a été supprimée
        self.assertFalse(self.artiste.style.is_connected(self.style1))
