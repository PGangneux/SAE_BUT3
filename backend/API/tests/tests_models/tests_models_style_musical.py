from neomodel.exceptions import UniqueProperty
from neomodel.exceptions import DoesNotExist
from ...tests import Neo4jTestCase
from ...models import StyleMusical
from neomodel import config


class StyleMusicalTestCase(Neo4jTestCase):

    def test_creation_style(self):
        """Test de création d'un style musical"""
        style = StyleMusical(name="Jazz").save()
        self.assertIsNotNone(style.uuid)
        self.assertEqual(style.name, "Jazz")

    def test_unique_name_constraint(self):
        """Test que le nom unique est respecté"""
        StyleMusical(name="Rock").save()
        with self.assertRaises(UniqueProperty):
            StyleMusical(name="Rock").save()

    def test_property_getters(self):
        """Test que les propriétés sont accessibles"""
        style = StyleMusical(name="Blues").save()
        # Getter direct
        self.assertEqual(style.name, "Blues")
        # Accès via .__dict__ ou .properties
        props = style.__properties__
        self.assertEqual(props['name'], "Blues")
        self.assertIsNotNone(props['uuid'])

    def test_update_property(self):
        """Test la mise à jour d'une propriété"""
        style = StyleMusical(name="Reggae").save()
        style.name = "Reggae Fusion"
        style.save()
        updated_style = StyleMusical.nodes.get(uuid=style.uuid)
        self.assertEqual(updated_style.name, "Reggae Fusion")

    def test_delete_style(self):
        """Test la suppression d'un style musical"""
        style = StyleMusical(name="Funk").save()
        uuid = style.uuid
        style.delete()
        with self.assertRaises(DoesNotExist):
            StyleMusical.nodes.get(uuid=uuid)

    def test_multiple_styles(self):
        """Test la création et récupération de plusieurs styles"""
        names = ["Salsa", "Hip-Hop", "Classical"]
        for n in names:
            StyleMusical(name=n).save()
        all_styles = [s.name for s in StyleMusical.nodes.all()]
        self.assertCountEqual(all_styles, names)
