from django.test import RequestFactory
from ...serializers import ArtisteSerializer
from ...errors import ValidatorUnique, NotFound
from ...models import Artiste, Nation
from ...tests import Neo4jTestCase


class ArtisteSerializerTests(Neo4jTestCase):
    """
    Tests du serializer ArtisteSerializer
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")

    def test_get_nation_returns_url_or_none(self):
        """Vérifie que get_nation renvoie correctement l'URL de la nation ou None"""
        nation = Nation(name="France").save()
        artiste = Artiste(name="Mylène Farmer").save()
        artiste.nationalite.connect(nation)

        serializer = ArtisteSerializer(artiste, context={"request": self.request})
        data = serializer.data
        self.assertIn("nation", data)
        self.assertIn(str(nation.uuid), data["nation"])

        # Cas sans nation
        artiste2 = Artiste(name="SansNation").save()
        serializer2 = ArtisteSerializer(artiste2, context={"request": self.request})
        data2 = serializer2.data
        self.assertIsNone(data2["nation"])

    def test_get_extraits_urls(self):
        """Vérifie que get_extraits renvoient des URLs valides"""
        artiste = Artiste(name="ArtistLinks").save()
        serializer = ArtisteSerializer(artiste, context={"request": self.request})
        data = serializer.data
        self.assertIn(str(artiste.uuid), data["extraits"])

    def test_create_success_with_nation(self):
        """Création d’un artiste avec rattachement à une nation"""
        nation = Nation(name="Japon").save()
        payload = {
            "name": "Hikaru Utada",
            "info": "Chanteuse",
            "nation_uuid": nation.uuid,
        }

        serializer = ArtisteSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        artiste = serializer.save()

        reloaded = Artiste.nodes.get(uuid=artiste.uuid)
        nations = [n.name for n in reloaded.nationalite.all()]
        self.assertEqual(nations, ["Japon"])

    def test_create_raises_uniqueproperty(self):
        """Création en doublon -> ValidatorUnique"""
        Artiste(name="Daft Punk").save()
        payload = {"name": "Daft Punk", "info": "duo"}

        serializer = ArtisteSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()

    def test_create_with_nonexistent_nation_raises_notfound(self):
        """Nation inexistante -> NotFound"""
        payload = {
            "name": "UnknownNationArtist",
            "nation_uuid": "00000000-0000-0000-0000-000000000000",
        }
        serializer = ArtisteSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    def test_update_success_and_nation_replace(self):
        """Mise à jour complète avec changement de nation"""
        artiste = Artiste(name="UpdateMe", info="Old info").save()
        n1 = Nation(name="Italie").save()
        n2 = Nation(name="Espagne").save()
        artiste.nationalite.connect(n1)

        payload = {"name": "UpdateMe", "nation_uuid": n2.uuid}
        serializer = ArtisteSerializer(
            instance=artiste, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()

        linked_nations = [n.name for n in updated.nationalite.all()]
        self.assertEqual(linked_nations, ["Espagne"])

    def test_update_raises_unique_on_conflict(self):
        """Tentative de renommage en un nom déjà existant -> ValidatorUnique"""
        a1 = Artiste(name="Existing1").save()
        a2 = Artiste(name="Existing2").save()

        payload = {"name": "Existing2", "info": "oops"}
        serializer = ArtisteSerializer(
            instance=a1, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()

    def test_update_with_nonexistent_nation_raises_notfound(self):
        """Lors de update(), si la nation fournie n'existe pas, on doit lever NotFound(Nation)."""
        # crée un artiste existant
        artiste = Artiste(name="WillUpdate", info="old").save()

        # payload avec une nation UUID qui n'existe pas
        payload = {
            "name": "WillUpdate",
            "info": "still old",
            "nation_uuid": "00000000-0000-0000-0000-000000000000",
        }

        serializer = ArtisteSerializer(
            instance=artiste, data=payload, context={"request": self.request}
        )
        assert serializer.is_valid(), serializer.errors

        with self.assertRaises(NotFound):
            serializer.save()
