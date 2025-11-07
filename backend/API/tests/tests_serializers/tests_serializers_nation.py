from django.test import RequestFactory

from ...serializers import NationSerializer, ValidatorUnique
from ...models import Nation
from ...tests import Neo4jTestCase


class NationSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/api/')

    # --- Méthodes de lecture ---
    def test_get_artistes_returns_correct_url(self):
        nation = Nation(name="France").save()
        serializer = NationSerializer(nation, context={'request': self.request})
        data = serializer.data
        self.assertIn(str(nation.uuid), data['artistes'])

    # --- Création ---
    def test_create_success(self):
        payload = {'name': 'Allemagne'}
        serializer = NationSerializer(data=payload, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        nation = serializer.save()
        reloaded = Nation.nodes.get(uuid=nation.uuid)
        self.assertEqual(reloaded.name, 'Allemagne')

    def test_create_raises_uniqueproperty(self):
        Nation(name="Italie").save()
        payload = {'name': 'Italie'}  # même nom -> UniqueProperty
        serializer = NationSerializer(data=payload, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()

    # --- Mise à jour ---
    def test_update_success(self):
        nation = Nation(name="Espagne").save()
        payload = {'name': 'EspagneMod'}
        serializer = NationSerializer(instance=nation, data=payload, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.name, 'EspagneMod')

    def test_update_raises_uniqueproperty(self):
        Nation(name="Portugal").save()
        nation = Nation(name="Belgique").save()
        payload = {'name': 'Portugal'}  # conflit de nom
        serializer = NationSerializer(instance=nation, data=payload, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()
