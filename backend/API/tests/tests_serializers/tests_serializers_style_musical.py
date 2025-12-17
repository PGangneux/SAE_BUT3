from django.test import RequestFactory

from ...serializers import StyleMusicalSerializer
from ...errors import ValidatorUnique
from ...models import StyleMusical
from ...tests import Neo4jTestCase


class StyleMusicalSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")

    # --- Méthodes de lecture ---
    def test_get_artistes_returns_correct_url(self):
        style = StyleMusical(name="Jazz").save()
        serializer = StyleMusicalSerializer(style, context={"request": self.request})
        data = serializer.data
        self.assertIn(str(style.uuid), data["artistes"])

    # --- Création ---
    def test_create_success(self):
        payload = {"name": "Rock"}
        serializer = StyleMusicalSerializer(
            data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        style = serializer.save()
        reloaded = StyleMusical.nodes.get(uuid=style.uuid)
        self.assertEqual(reloaded.name, "Rock")

    def test_create_raises_uniqueproperty(self):
        StyleMusical(name="Pop").save()
        payload = {"name": "Pop"}  # doublon
        serializer = StyleMusicalSerializer(
            data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()

    # --- Mise à jour ---
    def test_update_success(self):
        style = StyleMusical(name="Classique").save()
        payload = {"name": "ClassiqueMod"}
        serializer = StyleMusicalSerializer(
            instance=style, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.name, "ClassiqueMod")

    def test_update_raises_uniqueproperty(self):
        StyleMusical(name="Electro").save()
        style = StyleMusical(name="Techno").save()
        payload = {"name": "Electro"}  # conflit
        serializer = StyleMusicalSerializer(
            instance=style, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()
