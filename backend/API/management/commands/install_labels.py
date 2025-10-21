from django.core.management.base import BaseCommand
from neomodel import install_all_labels

class Command(BaseCommand):
    help = 'Crée tous les labels et contraintes uniques Neo4j pour les modèles StructuredNode'

    def handle(self, *args, **options):
        install_all_labels()
        self.stdout.write(self.style.SUCCESS('Tous les labels et contraintes Neo4j ont été créés !'))
