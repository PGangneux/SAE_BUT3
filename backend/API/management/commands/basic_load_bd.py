from datetime import date
from django.core.management.base import BaseCommand
from neomodel import db
from ...models import Artiste, Interview, Extrait, PositionExtraitRel, Question, StyleMusical, Theme, Utilisateur
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Charge la base de données avec des données simples'

    def handle(self, *args, **options):
        results, headers = db.cypher_query("MATCH (n) detach delete n")
        self.stdout.write(self.style.SUCCESS('Base de données supprimé'))
        theme = Theme(name="Thème 1", description="Thème de test n°1").save()
        question = Question(texte="Question 1").save()
        style = StyleMusical(name="Style Musical 1").save()
        artiste = Artiste(name="Artiste 1", info="Artiste de test n°1").save()
        interview = Interview(titre="Interview 1", date=date.today(), occasion="Festival de la Musique", description="Interview 1 de l'Artiste 1", lieu="Paris").save()
        extrait = Extrait(titre="Extrait 1", description="Extrait 1 de l'interview 1", youtube_url="youtube.com", vimeo_url= "vimeo.com", uploaded_at=date.today()).save()
        utilisateur = Utilisateur(pseudo="Test Utilisateur", prenom="Jean", nom="Dupond", email="test@exemple.com", password=make_password("testmdp")).save()

        question.theme.connect(theme)
        artiste.style.connect(style)
        interview.interviewer.connect(artiste)
        extrait.interview.connect(interview, {'position': 1})
        extrait.question.connect(question)
        self.stdout.write(self.style.SUCCESS('Base de données chargé'))