from neomodel import db
from django.core.management.base import BaseCommand
from neomodel import install_all_labels

class Command(BaseCommand):
    help = 'Crée tous les labels et contraintes uniques Neo4j pour les modèles StructuredNode'

    def handle(self, *args, **options):
        for row in db.cypher_query("SHOW CONSTRAINTS")[0]:
            name = row[1] if row[1] else row[0]
            if name:
                try:
                    query = f"DROP CONSTRAINT {name} IF EXISTS"
                    print(query)
                    db.cypher_query(query)
                    self.stdout.write(self.style.SUCCESS(f"Contrainte supprimée : {name}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erreur suppression contrainte {name}: {e}"))

        for row in db.cypher_query("SHOW INDEXES")[0]:
            name = row[1] if row[1] else row[0]
            if name:
                try:
                    query = f"DROP INDEX {name} IF EXISTS"
                    print(query)
                    db.cypher_query(query)
                    self.stdout.write(self.style.SUCCESS(f"Index supprimé : {name}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erreur suppression index {name}: {e}"))

        install_all_labels()
        self.stdout.write(self.style.SUCCESS('Tous les labels et contraintes Neo4j ont été créés !'))
