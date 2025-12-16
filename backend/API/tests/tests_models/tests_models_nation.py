from neomodel import db
from neomodel.exceptions import UniqueProperty
from neomodel.exceptions import DoesNotExist
from ...tests import Neo4jTestCase
from ...models import Artiste, Nation


class NationTestCase(Neo4jTestCase):

    def test_creation_nation(self):
        """Création simple d'une nation"""
        n = Nation(name="France").save()
        self.assertIsNotNone(n.uuid)
        self.assertEqual(n.name, "France")

    def test_unique_name_constraint(self):
        """Le nom de la nation doit être unique"""
        Nation(name="Espagne").save()
        with self.assertRaises(UniqueProperty):
            Nation(name="Espagne").save()

    def test_update_name(self):
        """Mise à jour du nom et vérification de la contrainte d'unicité"""
        n = Nation(name="Allemagne").save()
        n.name = "Allemagne - FR"
        n.save()
        reloaded = Nation.nodes.get(uuid=n.uuid)
        self.assertEqual(reloaded.name, "Allemagne - FR")

        # tenter de renommer sur un nom existant doit lever UniqueProperty
        Nation(name="Italie").save()
        reloaded.name = "Italie"
        with self.assertRaises(UniqueProperty):
            reloaded.save()

    def test_delete_nation(self):
        """Suppression d'une nation"""
        n = Nation(name="Portugal").save()
        uuid = n.uuid
        n.delete()
        with self.assertRaises(DoesNotExist):
            Nation.nodes.get(uuid=uuid)

    def test_filtering_and_properties(self):
        """Filtrage via nodes.filter() et accès aux propriétés via __properties__"""
        Nation(name="Belgique").save()
        Nation(name="Suisse").save()

        found = Nation.nodes.filter(name="Belgique")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, "Belgique")

        props = found[0].__properties__
        self.assertIn("uuid", props)
        self.assertEqual(props["name"], "Belgique")

    def test_relation_with_artiste_nationalite(self):
        """Vérifie qu'un Artiste peut être relié comme NATIONALITE -> Nation"""
        nation = Nation(name="Canada").save()
        artiste = Artiste(name="X").save()

        # Connecter l'artiste à la nation
        artiste.nationalite.connect(nation)

        # Vérifier via une requête Cypher qu'il existe une relation Artiste-[:NATIONALITE]->Nation
        result, _ = db.cypher_query(
            "MATCH (a:Artiste)-[:NATIONALITE]->(n:Nation {uuid:$uuid}) RETURN count(a)",
            {"uuid": nation.uuid},
        )
        self.assertEqual(int(result[0][0]), 1)

        # Déconnecter et vérifier qu'il n'y a plus de relation
        artiste.nationalite.disconnect(nation)
        result_after, _ = db.cypher_query(
            "MATCH (a:Artiste)-[:NATIONALITE]->(n:Nation {uuid:$uuid}) RETURN count(a)",
            {"uuid": nation.uuid},
        )
        self.assertEqual(int(result_after[0][0]), 0)
