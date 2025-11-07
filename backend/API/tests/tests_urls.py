from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from django.contrib.auth.hashers import make_password
from ..models import Artiste, Extrait, Interview, Utilisateur
from ..tests import Neo4jTestCase

class URLsAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()
        # Exemple UUID pour les URLs nécessitant un identifiant
        self.uuid = str(uuid4())

    def test_login_url(self):
        url = reverse('login')
        response = self.client.get(url)
        # GET n'est pas autorisé, POST attendu -> 405 METHOD NOT ALLOWED
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_token_refresh_url(self):
        url = reverse('token_refresh')
        response = self.client.post(url, data={"refresh": "fake_token"}, format='json')
        # Le token est invalide -> 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_theme_urls(self):
        self.assertEqual(self.client.get(reverse('theme-list')).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('theme-detail', kwargs={'uuid': self.uuid})).status_code, status.HTTP_404_NOT_FOUND)
        # Nested theme questions
        self.assertEqual(self.client.get(reverse('question-list', kwargs={'theme_uuid': self.uuid})).status_code, status.HTTP_200_OK)

    def test_question_urls(self):
        self.assertEqual(self.client.get(reverse('question-list')).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('question-detail', kwargs={'uuid': self.uuid})).status_code, status.HTTP_404_NOT_FOUND)
        # Nested question extraits
        self.assertEqual(self.client.get(reverse('extrait-list', kwargs={'question_uuid': self.uuid})).status_code, status.HTTP_200_OK)

    def test_extrait_urls(self):
        self.extrait = Extrait(duree=120).save()
        self.assertEqual(self.client.get(reverse('extrait-list')).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('extrait-detail', kwargs={'uuid': self.extrait.uuid})).status_code, status.HTTP_200_OK)
        # Nested extrait relationships
        self.assertEqual(self.client.get(reverse('interview-list', kwargs={'extrait_uuid': self.extrait.uuid})).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('tag-list', kwargs={'extrait_uuid': self.extrait.uuid})).status_code, status.HTTP_200_OK)

    def test_interview_urls(self):
        self.interview = Interview(titre=f"Test{uuid4()}").save()
        self.assertEqual(self.client.get(reverse('interview-list')).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('interview-detail', kwargs={'uuid': self.interview.uuid})).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('extrait-list', kwargs={'interview_uuid': self.interview.uuid})).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('tag-list', kwargs={'interview_uuid': self.interview.uuid})).status_code, status.HTTP_200_OK)

    def test_artiste_urls(self):
        self.artiste = Artiste(name="Test").save()
        self.assertEqual(self.client.get(reverse('artiste-list')).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('artiste-detail', kwargs={'uuid': self.artiste.uuid})).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('extrait-list', kwargs={'artiste_uuid': self.artiste.uuid})).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('style-list', kwargs={'artiste_uuid': self.artiste.uuid})).status_code, status.HTTP_200_OK)

    def test_styles_musical_urls(self):
        self.assertEqual(self.client.get(reverse('style-musical-list')).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('style-musical-detail', kwargs={'uuid': self.uuid})).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.get(reverse('artiste-list', kwargs={'stylemusical_uuid': self.uuid})).status_code, status.HTTP_200_OK)

    def test_nation_urls(self):
        self.assertEqual(self.client.get(reverse('nation-list')).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('nation-detail', kwargs={'uuid': self.uuid})).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.get(reverse('artiste-list', kwargs={'nation_uuid': self.uuid})).status_code, status.HTTP_200_OK)

    def test_tag_urls(self):
        self.assertEqual(self.client.get(reverse('tag-list')).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('tag-detail', kwargs={'uuid': self.uuid})).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.get(reverse('extrait-list', kwargs={'tag_uuid': self.uuid})).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('interview-list', kwargs={'tag_uuid': self.uuid})).status_code, status.HTTP_200_OK)

    def test_utilisateur_urls(self):
        self.utilisateur = Utilisateur(
            pseudo=f"user_{uuid4()}",
            prenom=f"Dupond {uuid4()} du nom",
            nom=f"de l'arbre à {uuid4} feuilles",
            email=f"user_{uuid4()}@example.com",
            password=make_password("password123")  # mot de passe hashé
        ).save()
        self.assertEqual(self.client.get(reverse('utilisateur-list')).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('utilisateur-detail', kwargs={'uuid': self.uuid})).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.get(reverse('artiste-list', kwargs={'utilisateur_uuid': self.utilisateur.uuid})).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('interview-list', kwargs={'utilisateur_uuid': self.utilisateur.uuid})).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('extrait-list', kwargs={'utilisateur_uuid': self.utilisateur.uuid})).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse('question-list', kwargs={'utilisateur_uuid': self.utilisateur.uuid})).status_code, status.HTTP_200_OK)
