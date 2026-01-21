# views.py
import csv
import io
from datetime import date as Date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from ..models import Artiste, Audio, Question, Tag, Theme

from ..serializers import (
    ArtisteSerializer,
    ThemeSerializer,
    QuestionSerializer,
    TagSerializer,
    ExtraitSerializer,
    AudioSerializer,
    OccasionSerializer,
    AudiosSerializer,
    TagsExtraitRelationShipSerializer,
)


class CSVImportView(APIView):
    """
    Permet d'importer un fichier CSV contenant des extraits d'interviews.
    """

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get("file")

        if not csv_file:
            return Response(
                {"error": "Aucun fichier envoyé"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Vérification basique
        if not csv_file.name.endswith(".csv"):
            return Response(
                {"error": "Le fichier doit être un CSV"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.save_data(csv_file)

        return Response(
            {"message": "lignes importées avec succès"}, status=status.HTTP_201_CREATED
        )

    def save_data(self, csv_file):
        # Lecture du fichier (UTF-8 recommandé)
        data = csv_file.read().decode("utf-8")
        io_string = io.StringIO(data)

        reader = csv.DictReader(io_string)

        for row in reader:
            print(row)  # Pour debug
            print(type(row))  # Pour debug
            self.save_row(row)

    def save_row(self, row):
        serializer_artiste = ArtisteSerializer()
        artiste = row["Artiste"].strip()
        artiste_uuid = None
        if artiste != "" and artiste is not None:
            try:
                artiste_uuid = serializer_artiste.create({"name": artiste}).uuid
            except:
                artiste_uuid = Artiste.nodes.get(name=artiste).uuid


        serializer_question = QuestionSerializer()
        question = row["Question"].strip()
        question_uuid = None
        if question != "" and question is not None:
            try:
                question_uuid = serializer_question.create(
                    {"texte": question}
                ).uuid
            except:
                question_uuid = Question.nodes.get(texte=question).uuid


        serializer_occasion = OccasionSerializer()
        evenement = row["Evenement"].strip()
        evenement_uuid = None
        if evenement != "" and evenement is not None:
            try:
                evenement_uuid = serializer_occasion.create({"name": evenement}).uuid
            except:
                evenement_uuid = None

        serializer_tag = TagSerializer()
        tags = [tag.strip() for tag in row["Tags"].split("; ")]
        tags_uuids = []
        for tag in tags:
            if tag != "" and tag is not None:
                try:
                    tag_uuid = serializer_tag.create({"name": tag}).uuid
                except:
                    tag_uuid = Tag.nodes.get(name=tag).uuid
                tags_uuids.append(tag_uuid)

        serializer_audio = AudioSerializer()
        audios = [audio.strip() for audio in row["Audios"].split("; ")]
        audios_uuids = []
        for audio in audios:
            if audio != "" and audio is not None:
                try:
                    audio_uuid = serializer_audio.create({"name": audio}).uuid
                except:
                    audio_uuid = Audio.nodes.get(name=audio).uuid
                    audios_uuids.append(audio_uuid)

        youtube_url = self.get_code(row["Youtube"].strip())

        date = row["Date"].strip()
        titre = artiste + " - " + evenement + " - " + question + " - " + date
        serializer_extrait = ExtraitSerializer()
        try:
            extrait_node = serializer_extrait.create(
                {
                    "titre": titre,
                    "artiste_uuid": artiste_uuid,
                    "question_uuid": question_uuid,
                    "uploaded_at": Date(date) if date != "" else None,
                    "lieu": row["Ville"].strip(),
                    "youtube_url": youtube_url,
                    "vimeo_url": row["Vimeo"].strip(),
                    "position": int(row["Position"].strip()) if row["Position"].strip() != "" else None,
                    "duree": 0,
                    "description": "",
                }
            )

            context = {"extrait": extrait_node}
            for audio_uuid in audios_uuids:
                serializer = AudiosSerializer(
                    data={"uuid": audio_uuid}, context=context
                )
                if serializer.is_valid():
                    serializer.create(serializer.validated_data)

            for tag_uuid in tags_uuids:
                serializer = TagsExtraitRelationShipSerializer(
                    data={"uuid": tag_uuid}, context=context
                )
                if serializer.is_valid():
                    serializer.create(serializer.validated_data)

        except Exception as e:
            print(f"Erreur lors de la création de l'extrait: {e}")

    def get_code(self, url):
        """
        Extrait le code vidéo d'une URL YouTube.
        """
        if "youtube.com/watch?v=" in url:
            return url.split("v=")[1]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1]
        return url
