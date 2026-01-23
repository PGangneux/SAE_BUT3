# views.py
import csv
import io
from datetime import date as Date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status





from ..models import Artiste, Audio, Occasion, Question, Tag, Theme

from ..serializers import (
    ArtisteSerializer,
    QuestionSerializer,
    TagSerializer,
    ExtraitSerializer,
    AudioSerializer,
    OccasionSerializer,
    AudiosSerializer,
    TagsExtraitRelationShipSerializer,
    InterviewSerializer,
    InterviewsSerializer,
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


        artiste = None
        occasion = None
        liste_extraits = []
        for row in reader:
            print(row)
            if artiste != None:
                if (artiste != row["Artiste"].strip() or occasion != row["Evenement"].strip()):
                    print("iiiiiiiiiiiiiiiii")
                    self.save_interview(liste_extraits, occasion)
                    liste_extraits = []
                    artiste = row["Artiste"].strip()
                    occasion = row["Evenement"].strip()
            else: 
                artiste = row["Artiste"].strip()
                occasion = row["Evenement"].strip()

            extrait = self.save_row(row)
            liste_extraits.append(extrait)

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
            
            return extrait_node

        except Exception as e:
            print(f"Erreur lors de la création de l'extrait: {e}")

    
    def save_interview(self, liste_extraits, occasion):
        if not liste_extraits:
            return

        serializer_interview = InterviewSerializer()
        first_extrait = liste_extraits[0]
        artiste_node = first_extrait.interviewer.single()

        serializer_occasion = OccasionSerializer()
        if occasion != "" and occasion is not None:
            try:
                occasion_node = serializer_occasion.create(
                    {"name": occasion}
                )
            except:
                occasion_node = Occasion.nodes.get(name=occasion)

        titre = f"Interview de {artiste_node.name} pour {occasion_node.name if occasion_node else 'une occasion inconnue'}"
        try:
            interview_node = serializer_interview.create(
                {
                    "titre": titre,
                    "date": first_extrait.uploaded_at,
                    "description": "",
                    "occasion_uuid": occasion_node.uuid if occasion_node else None,
                }
            )

            for extrait in liste_extraits:
                context = {"extrait": extrait}
                serializer = InterviewsSerializer(
                    data={"uuid": interview_node.uuid, "position":extrait.position}, context=context
                )
                if serializer.is_valid():
                    serializer.create(serializer.validated_data)

        except Exception as e:
            print(f"Erreur lors de la création de l'interview: {e}")
    
    def get_code(self, url):
        """
        Extrait le code vidéo d'une URL YouTube.
        """
        if "youtube.com/watch?v=" in url:
            return url.split("v=")[1]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1]
        return url
