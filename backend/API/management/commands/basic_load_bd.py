from datetime import date
from django.core.management.base import BaseCommand
from neomodel import db
from ...models import (
    Artiste,
    Interview,
    Extrait,
    Question,
    StyleMusical,
    Tag,
    Theme,
    Utilisateur,
)
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    """
    Permet de charger la base de données avec des données de test
    """

    help = "Charge la base de données avec des données simples"

    def handle(self, *args, **options):
        db.cypher_query("MATCH (n) detach delete n")
        self.stdout.write(self.style.SUCCESS("Base de données supprimé"))
        theme = Theme(uuid=1, name="Thème 1", description="Thème de test n°1").save()
        question = Question(uuid=1, texte="Question 1").save()
        style = StyleMusical(uuid=1, name="Style Musical 1").save()
        artiste = Artiste(uuid=1, name="Artiste 1", info="Artiste de test n°1").save()
        artiste2 = Artiste(uuid=2, name="Artiste 2", info="Artiste de test n°2").save()
        interview = Interview(
            uuid=1000,
            titre="Interview 1",
            date=date.today(),
            occasion="Festival de la Musique",
            description="Interview 1 de l'Artiste 1",
            lieu="Paris",
        ).save()
        interview2 = Interview(
            uuid=1001,
            titre="Interview 2",
            date=date.today(),
            occasion="Festival de la Musique Orléans",
            description="Interview 2 de l'Artiste 2",
            lieu="Orléans",
        ).save()
        tag = Tag(uuid=1, name="Test Tag").save()
        utilisateur = Utilisateur(
            uuid=1,
            pseudo="Test Utilisateur",
            prenom="Jean",
            nom="Dupond",
            email="test@exemple.com",
            password=make_password("testmdp"),
        ).save()
        admin = Utilisateur(
            uuid=2,
            pseudo="Test Admin",
            prenom="Ano",
            nom="Nyme",
            email="admin@exemple.com",
            password=make_password("adminmdp"),
            is_admin=True,
        ).save()

        extrait1 = Extrait(
            uuid=1,
            titre="Extrait 1",
            description="Extrait 1 de l'interview 1",
            youtube_url="1NYQ65FTEC8",
            vimeo_url="1128762950",
            uploaded_at=date.today(),
            duree=30,
        ).save()
        extrait2 = Extrait(
            uuid=2,
            titre="Extrait 2",
            description="Extrait 2 de l'interview 1",
            youtube_url="ux6ZtL1o0R0",
            vimeo_url="1128763050",
            uploaded_at=date.today(),
            duree=37,
        ).save()
        extrait3 = Extrait(
            uuid=3,
            titre="Extrait 3",
            description="Extrait 3 de l'interview 1",
            youtube_url="WpFoiw2uP0w",
            vimeo_url="1128763155",
            uploaded_at=date.today(),
            duree=149,
        ).save()
        extrait4 = Extrait(
            uuid=4,
            titre="Extrait 4",
            description="Extrait 4 de l'interview 1",
            youtube_url="2PDvQ3P8c64",
            vimeo_url="1128763765",
            uploaded_at=date.today(),
            duree=108,
        ).save()

        extrait5 = Extrait(
            uuid=5,
            titre="Extrait 5",
            description="Extrait 1 de l'interview 2",
            youtube_url="9eLoUEBF6no",
            vimeo_url="1128786403",
            uploaded_at=date.today(),
            duree=30,
        ).save()
        extrait6 = Extrait(
            uuid=6,
            titre="Extrait 6",
            description="Extrait 2 de l'interview 2",
            youtube_url="Wt14RXtzZxI",
            vimeo_url="1128786928",
            uploaded_at=date.today(),
            duree=37,
        ).save()
        extrait7 = Extrait(
            uuid=7,
            titre="Extrait 7",
            description="Extrait 3 de l'interview 2",
            youtube_url="IqLw5KDf9Fg",
            vimeo_url="1128788337",
            uploaded_at=date.today(),
            duree=149,
        ).save()
        extrait8 = Extrait(
            uuid=8,
            titre="Extrait 8",
            description="Extrait 4 de l'interview 2",
            youtube_url="uwIyaln-k8A",
            vimeo_url="1128790175",
            uploaded_at=date.today(),
            duree=108,
        ).save()
        extrait9 = Extrait(
            uuid=9,
            titre="Extrait 9",
            description="Extrait 5 de l'interview 2",
            youtube_url="10MZrDXjby8",
            vimeo_url=None,
            uploaded_at=date.today(),
            duree=30,
        ).save()
        extrait10 = Extrait(
            uuid=10,
            titre="Extrait 10",
            description="Extrait 6 de l'interview 2",
            youtube_url="dUTuetpJ8_o",
            vimeo_url=None,
            uploaded_at=date.today(),
            duree=37,
        ).save()
        extrait11 = Extrait(
            uuid=11,
            titre="Extrait 11",
            description="Extrait 7 de l'interview 2",
            youtube_url="8GT8LUC1-EU",
            vimeo_url=None,
            uploaded_at=date.today(),
            duree=149,
        ).save()
        extrait12 = Extrait(
            uuid=12,
            titre="Extrait 12",
            description="Extrait 8 de l'interview 2",
            youtube_url="PO7FDDthezY",
            vimeo_url=None,
            uploaded_at=date.today(),
            duree=108,
        ).save()

        question.theme.connect(theme)
        artiste.style.connect(style)
        artiste2.style.connect(style)
        extrait1.interviews.connect(interview, {"position": 0})
        extrait2.interviews.connect(interview, {"position": 1})
        extrait3.interviews.connect(interview, {"position": 2})
        extrait4.interviews.connect(interview, {"position": 3})
        extrait1.interviewer.connect(artiste)
        extrait2.interviewer.connect(artiste)
        extrait3.interviewer.connect(artiste)
        extrait4.interviewer.connect(artiste)
        extrait1.question.connect(question)
        extrait2.question.connect(question)
        interview.tags_interview.connect(tag)
        extrait1.tags_extrait.connect(tag)

        extrait5.interviews.connect(interview2, {"position": 0})
        extrait6.interviews.connect(interview2, {"position": 1})
        extrait7.interviews.connect(interview2, {"position": 2})
        extrait8.interviews.connect(interview2, {"position": 3})
        extrait9.interviews.connect(interview2, {"position": 4})
        extrait10.interviews.connect(interview2, {"position": 5})
        extrait11.interviews.connect(interview2, {"position": 6})
        extrait12.interviews.connect(interview2, {"position": 7})
        extrait5.interviewer.connect(artiste2)
        extrait6.interviewer.connect(artiste2)
        extrait7.interviewer.connect(artiste2)
        extrait8.interviewer.connect(artiste2)
        extrait9.interviewer.connect(artiste2)
        extrait10.interviewer.connect(artiste2)
        extrait11.interviewer.connect(artiste2)
        extrait12.interviewer.connect(artiste2)
        extrait9.question.connect(question)
        extrait10.question.connect(question)
        interview2.tags_interview.connect(tag)
        extrait9.tags_extrait.connect(tag)

        utilisateur.recherches_artistes.connect(artiste)
        utilisateur.regarder_interviews.connect(interview)
        utilisateur.regarder_extraits.connect(extrait1)
        utilisateur.recherches_questions.connect(question)
        self.stdout.write(self.style.SUCCESS("Base de données chargé"))
