from datetime import date
from django.core.management.base import BaseCommand
from neomodel import db
from ...models import Artiste, Interview, Extrait, Nation, PositionExtraitRel, Question, StyleMusical, Tag, Theme, Utilisateur
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
        nation = Nation(name="Test Nation").save()
        tag = Tag(name="Test Tag").save()
        utilisateur = Utilisateur(pseudo="Test Utilisateur", prenom="Jean", nom="Dupond", email="test@exemple.com", password=make_password("testmdp")).save()

        extrait1 = Extrait(titre="Extrait 1", description="Extrait 1 de l'interview 1", youtube_url="https://www.youtube.com/embed/1NYQ65FTEC8?si=gwQlb9W4mPKm9Ri-", vimeo_url= "https://player.vimeo.com/video/1128762950?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479", uploaded_at=date.today()).save()
        extrait2 = Extrait(titre="Extrait 2", description="Extrait 2 de l'interview 1", youtube_url="https://www.youtube.com/embed/ux6ZtL1o0R0?si=lH7-5QMdNo028Lrr", vimeo_url= "https://player.vimeo.com/video/1128763050?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479", uploaded_at=date.today()).save()
        extrait3 = Extrait(titre="Extrait 3", description="Extrait 3 de l'interview 1", youtube_url="https://www.youtube.com/embed/WpFoiw2uP0w?si=bTHhoTddKjCwC5lL", vimeo_url= "https://player.vimeo.com/video/1128763155?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479", uploaded_at=date.today()).save()
        extrait4 = Extrait(titre="Extrait 4", description="Extrait 4 de l'interview 1", youtube_url="https://www.youtube.com/embed/2PDvQ3P8c64?si=8k335KO41AROxbZu", vimeo_url= "https://player.vimeo.com/video/1128763765?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479", uploaded_at=date.today()).save()
        

        question.theme.connect(theme)
        artiste.style.connect(style)
        artiste.nationalite.connect(nation)
        interview.interviewer.connect(artiste)
        extrait1.interview.connect(interview, {'position': 1})
        extrait2.interview.connect(interview, {'position': 2})
        extrait3.interview.connect(interview, {'position': 3})
        extrait4.interview.connect(interview, {'position': 4})
        extrait1.question.connect(question)
        interview.tags_interview.connect(tag)
        extrait1.tags_extrait.connect(tag)
        self.stdout.write(self.style.SUCCESS('Base de données chargé'))