from neomodel.exceptions import UniqueProperty
from neomodel.exceptions import DoesNotExist
from ...tests import Neo4jTestCase
from ...models import Artiste, Nation


class ArtisteTestCase(Neo4jTestCase):
    def test_creation_artiste(self):
        """Création simple d'un artiste"""
        artiste = Artiste(
            name="Daft Punk", info="Groupe de musique électronique"
        ).save()
        self.assertIsNotNone(artiste.uuid)
        self.assertEqual(artiste.name, "Daft Punk")
        self.assertEqual(artiste.info, "Groupe de musique électronique")

    def test_unique_name_constraint(self):
        """Le nom d'artiste doit être unique"""
        Artiste(name="Stromae").save()
        with self.assertRaises(UniqueProperty):
            Artiste(name="Stromae").save()

    def test_update_info(self):
        """Mise à jour des propriétés"""
        artiste = Artiste(name="M").save()
        artiste.info = "Auteur-compositeur-interprète français"
        artiste.save()
        updated = Artiste.nodes.get(uuid=artiste.uuid)
        self.assertEqual(updated.info, "Auteur-compositeur-interprète français")

    def test_delete_artiste(self):
        """Suppression d'un artiste"""
        artiste = Artiste(name="Aya Nakamura").save()
        uuid = artiste.uuid
        artiste.delete()
        with self.assertRaises(DoesNotExist):
            Artiste.nodes.get(uuid=uuid)

    def test_relation_nationalite(self):
        """Test de la relation NATIONALITE (Artiste → Nation)"""
        artiste = Artiste(name="Shakira").save()
        colombie = Nation(name="Colombie").save()
        france = Nation(name="France").save()

        artiste.nationalite.connect(colombie)
        # On remplace la nationalité unique
        artiste.nationalite.disconnect(colombie)
        artiste.nationalite.connect(france)

        connected_nations = [n.name for n in artiste.nationalite.all()]
        self.assertEqual(len(connected_nations), 1)
        self.assertEqual(connected_nations[0], "France")

    def test_getters_and_properties(self):
        """Test d'accès aux propriétés"""
        artiste = Artiste(name="Orelsan", info="Rappeur français").save()
        props = artiste.__properties__
        self.assertIn("uuid", props)
        self.assertEqual(props["name"], "Orelsan")
        self.assertEqual(props["info"], "Rappeur français")

    def test_filtering_and_queries(self):
        """Test de récupération et filtrage"""
        Artiste(name="Booba").save()
        Artiste(name="PNL").save()
        results = Artiste.nodes.filter(name="Booba")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Booba")
