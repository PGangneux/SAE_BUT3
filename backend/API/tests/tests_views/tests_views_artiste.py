from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Artiste, StyleMusical, Nation
from ...tests import Neo4jTestCase

class ArtisteViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()
        self.artiste1 = Artiste(name="John Doe", info="info1").save()
        self.artiste2 = Artiste(name="Jane Smith", info="info2").save()

    def test_list_artistes(self):
        url = reverse('artiste-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(a['uuid'] == self.artiste1.uuid for a in response.json()))
        self.assertTrue(any(a['uuid'] == self.artiste2.uuid for a in response.json()))

    def test_retrieve_artiste(self):
        url = reverse('artiste-detail', kwargs={'uuid': self.artiste1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['uuid'], self.artiste1.uuid)

    def test_retrieve_nonexistent_artiste(self):
        url = reverse('artiste-detail', kwargs={'uuid': '00000000-0000-0000-0000-000000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_artistes(self):
        url = reverse('artiste-list') + "?search=Jane"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['uuid'], self.artiste2.uuid)
    
    def test_order_asc_artistes_OK(self):
        url = reverse('artiste-list')
        response = self.client.get(url + '?order=name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['uuid'], self.artiste2.uuid)
    
    def test_order_desc_artistes_OK(self):
        url = reverse('artiste-list')
        response = self.client.get(url + '?order=-name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['uuid'], self.artiste1.uuid)

    def test_order_artistesKO(self):
        url = reverse('artiste-list')
        response = self.client.get(url + '?order=testtest')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("Order error", data.keys())
        self.assertEqual("testtest", data["Order error"])
    
    def test_order_asc_artistes_relationship_nodesOK(self):
        self.artiste1.style.connect(StyleMusical(name="Style A").save())
        self.artiste2.style.connect(StyleMusical(name="Style B").save())
        url = reverse('artiste-list')
        response = self.client.get(url + '?order=style__name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['uuid'], self.artiste1.uuid)
    
    def test_order_desc_artistes_relationship_nodesOK(self):
        self.artiste1.style.connect(StyleMusical(name="Style A").save())
        self.artiste2.style.connect(StyleMusical(name="Style B").save())
        url = reverse('artiste-list')
        response = self.client.get(url + '?order=-style__name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['uuid'], self.artiste2.uuid)

    def test_order_artistes_relationship_KO(self):
        url = reverse('artiste-list')
        response = self.client.get(url + '?order=testttest__test')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("Order error", data.keys())
        self.assertEqual("testttest", data["Order error"])

    def test_order_artistes_relationship_nodesKO(self):
        self.artiste1.style.connect(StyleMusical(name="Style A").save())
        url = reverse('artiste-list')
        response = self.client.get(url + '?order=style__test')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("Order error", data.keys())
        self.assertEqual("test", data["Order error"])
    
    def test_pagination_artistes_sizeOK(self):
        url = reverse("artiste-list")
        response = self.client.get(url + "?size=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(len(Artiste.nodes), 2)
    
    def test_pagination_artistes_wrong_sizeOK(self):
        url = reverse("artiste-list")
        response = self.client.get(url + "?size=0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(len(Artiste.nodes), 2)
    
    def test_pagination_artistes_size1_page2OK(self):
        url = reverse("artiste-list")
        response = self.client.get(url + "?size=1&page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(len(Artiste.nodes), 2)

    def test_pagination_artistes_size_empty(self):
        url = reverse("artiste-list")
        response = self.client.get(url + "?size=150&page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 0)
        self.assertEqual(len(Artiste.nodes), 2)

    def test_pagination_artistes_size_not_int(self):
        url = reverse("artiste-list")
        response = self.client.get(url + "?size=test&page=2")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pagination_artistes_page_not_int(self):
        url = reverse("artiste-list")
        response = self.client.get(url + "?size=1&page=test")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_skip_artistesOK(self):
        url = reverse("artiste-list")
        response = self.client.get(url + "?skip=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)

    def test_skip_artistesKO(self):
        url = reverse("artiste-list")
        response = self.client.get(url + "?skip=test")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StyleMusicalArtisteViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()
        self.artiste = Artiste(name=f"Artiste_{uuid4()}", info="info").save()
        self.style = StyleMusical(name=f"Style_{uuid4()}").save()
        self.artiste.style.connect(self.style)

    def test_list_artistes_by_style(self):
        url = reverse('artiste-list', kwargs={'stylemusical_uuid': self.style.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(a['uuid'] == self.artiste.uuid for a in response.json()))

    def test_retrieve_artiste_by_style(self):
        url = reverse('artiste-detail', kwargs={'stylemusical_uuid': self.style.uuid, 'uuid': self.artiste.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['uuid'], self.artiste.uuid)

    def test_retrieve_nonexistent_artiste_by_style(self):
        url = reverse('artiste-detail', kwargs={'stylemusical_uuid': self.style.uuid, 'uuid': '00000000-0000-0000-0000-000000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NationArtisteViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()
        self.artiste = Artiste(name=f"Artiste_{uuid4()}", info="info").save()
        self.nation = Nation(name=f"Nation_{uuid4()}").save()
        self.artiste.nationalite.connect(self.nation)

    def test_list_artistes_by_nation(self):
        url = reverse('artiste-list', kwargs={'nation_uuid': self.nation.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(a['uuid'] == self.artiste.uuid for a in response.json()))

    def test_retrieve_artiste_by_nation(self):
        url = reverse('artiste-detail', kwargs={'nation_uuid': self.nation.uuid, 'uuid': self.artiste.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['uuid'], self.artiste.uuid)

    def test_retrieve_nonexistent_artiste_by_nation(self):
        url = reverse('artiste-detail', kwargs={'nation_uuid': self.nation.uuid, 'uuid': '00000000-0000-0000-0000-000000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
