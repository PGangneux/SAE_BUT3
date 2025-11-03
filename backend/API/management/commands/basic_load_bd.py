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
        theme = Theme(uuid=1, name="Thème 1", description="Thème de test n°1").save()
        question = Question(uuid=1, texte="Question 1").save()
        style = StyleMusical(uuid=1, name="Style Musical 1").save()
        artiste = Artiste(uuid=1, name="Artiste 1", info="Artiste de test n°1").save()
        interview = Interview(uuid=1, titre="Interview 1", date=date.today(), occasion="Festival de la Musique", description="Interview 1 de l'Artiste 1", lieu="Paris").save()
        nation = Nation(uuid=1, name="Test Nation").save()
        tag = Tag(uuid=1, name="Test Tag").save()
        utilisateur = Utilisateur(uuid=1, pseudo="Test Utilisateur", prenom="Jean", nom="Dupond", email="test@exemple.com", password=make_password("testmdp")).save()
        admin = Utilisateur(uuid=2, pseudo="Test Admin", prenom="Ano", nom="Nyme", email="admin@exemple.com", password=make_password("adminmdp"), is_admin=True).save()

        extrait1 = Extrait(uuid=1, titre="Extrait 1", description="Extrait 1 de l'interview 1", youtube_url="1NYQ65FTEC8", vimeo_url= "1128762950", uploaded_at=date.today(), duree=30).save()
        extrait2 = Extrait(uuid=2, titre="Extrait 2", description="Extrait 2 de l'interview 1", youtube_url="ux6ZtL1o0R0", vimeo_url= "1128763050", uploaded_at=date.today(), duree=37).save()
        extrait3 = Extrait(uuid=3, titre="Extrait 3", description="Extrait 3 de l'interview 1", youtube_url="WpFoiw2uP0w", vimeo_url= "1128763155", uploaded_at=date.today(), duree=149).save()
        extrait4 = Extrait(uuid=4, titre="Extrait 4", description="Extrait 4 de l'interview 1", youtube_url="2PDvQ3P8c64", vimeo_url= "1128763765", uploaded_at=date.today(), duree=108).save()


        question.theme.connect(theme)
        artiste.style.connect(style)
        artiste.nationalite.connect(nation)
        extrait1.interviews.connect(interview, {'position': 0})
        extrait2.interviews.connect(interview, {'position': 1})
        extrait3.interviews.connect(interview, {'position': 2})
        extrait4.interviews.connect(interview, {'position': 3})
        extrait1.interviewer.connect(artiste)
        extrait2.interviewer.connect(artiste)
        extrait3.interviewer.connect(artiste)
        extrait4.interviewer.connect(artiste)
        extrait1.question.connect(question)
        extrait2.question.connect(question)
        interview.tags_interview.connect(tag)
        extrait1.tags_extrait.connect(tag)
        utilisateur.recherches_artistes.connect(artiste)
        utilisateur.regarder_interviews.connect(interview)
        utilisateur.regarder_extraits.connect(extrait1)
        utilisateur.recherches_questions.connect(question)
        self.stdout.write(self.style.SUCCESS('Base de données chargé'))