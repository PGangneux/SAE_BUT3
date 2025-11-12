from django.test import RequestFactory
from uuid import uuid4
from ...serializers import StyleRelationShipSerializer
from ...errors import ContextError, NotFound
from ...models import Artiste, StyleMusical
from ...tests import Neo4jTestCase


class StyleRelationShipSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/api/')
        self.artiste = Artiste(
            name=f"Artiste_{uuid4()}",
            info="Info"
        ).save()
        self.style = StyleMusical(name=f"Style_{uuid4()}").save()

    # --- Getters ---
    def test_get_artistes_returns_url(self):
        serializer = StyleRelationShipSerializer(self.style, context={'request': self.request, 'artiste': self.artiste})
        url = serializer.get_artistes(self.style)
        self.assertIn(str(self.style.uuid), url)

    # --- create ---
    def test_create_connects_style_to_artiste(self):
        serializer = StyleRelationShipSerializer(
            data={'uuid': self.style.uuid},
            context={'artiste': self.artiste, 'request': self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        style = serializer.save()
        self.assertEqual(style.uuid, self.style.uuid)
        self.assertTrue(self.artiste.style.is_connected(self.style))

    def test_create_raises_contexterror_without_artiste(self):
        serializer = StyleRelationShipSerializer(data={'uuid': self.style.uuid}, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ContextError):
            serializer.save()

    def test_create_raises_notfound_with_invalid_uuid(self):
        serializer = StyleRelationShipSerializer(
            data={'uuid': '00000000-0000-0000-0000-000000000000'},
            context={'artiste': self.artiste, 'request': self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    # --- delete ---
    def test_delete_disconnects_style_from_artiste(self):
        self.artiste.style.connect(self.style)
        serializer = StyleRelationShipSerializer(context={'artiste': self.artiste, 'request': self.request})
        style = serializer.delete(self.style.uuid)
        self.assertEqual(style.uuid, self.style.uuid)
        self.assertFalse(self.artiste.style.is_connected(self.style))

    def test_delete_raises_contexterror_without_artiste(self):
        serializer = StyleRelationShipSerializer(context={'request': self.request})
        with self.assertRaises(ContextError):
            serializer.delete(self.style.uuid)

    def test_delete_raises_notfound_with_invalid_uuid(self):
        serializer = StyleRelationShipSerializer(context={'artiste': self.artiste, 'request': self.request})
        with self.assertRaises(NotFound):
            serializer.delete('00000000-0000-0000-0000-000000000000')
