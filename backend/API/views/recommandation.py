import json
from django.http import HttpRequest, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from neomodel import NodeSet, db
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import ExpiredTokenError
from ..models import Extrait, Interview, Utilisateur, StructuredNode
from ..serializers import ExtraitSerializer, InterviewSerializer

from rest_framework.exceptions import NotAuthenticated, ValidationError
from neo4j.graph import Node
from neo4j.exceptions import ServiceUnavailable
from ..errors import ConnexionDB


class Recommandation(APIView):
    """
    Actuel:
        Vidéo similaire à celle en cours
        Créer un score à partir des poids de Thèmes, Artistes et Questions en commun avec la vidéo regarder
        Trier par score puis par récente
        Non visionner si connecter

    Objectif:
        TODO get x derniers Interview/extrait regardés
        TODO filtrer celles avec watch time > 70%
        TODO - proposées proportion interview/extratait en fonction de ce que l'utilisateur regarde le plus
            si user regarde plus extrait commencé par proposées x extraits, max 4 extrait 1 interview vise versa
            donc 4 pour 1 max pour choisir extrait/interview on fait classement de tags des x derniers regardés sup 70%
        classement des thèmes
        classement des artistes
        classement des questions
        TODO regarder le chemin d'entrée sur le lecteur video
            TODO si c'est par une playlist on propose plus d'interview
            TODO si c'est par une question on propose plus d'extrait
            si c'est par artiste on ajoute un poids sur ce classement des artistes
            si c'est par thème  on ajoute un poids sur ce classement des thèmes
        TODO si pas de user ou pas assez de data on propose les video les plus regardé / récentes
        caper le nombre de données récupérées
        récupérer égalment les interviews
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request: HttpRequest):
        return self.post(request)

    def post(self, request: HttpRequest):
        poids: dict = request.data
        print("poids:", poids)

        user = get_current_user(request)
        print("user: ", user.pseudo if user else None)

        context = {"request": request}

        video = request.GET.get("video", None)
        size: str = request.GET.get("size", "10")
        if size.isnumeric():
            try:
                size: int = int(size)
            except:
                raise ValidationError(detail='{size: numeric not string}')

        # Modulabilité du modèle
        video_class = Extrait.__name__
        playlist_class= Interview.__name__

        print('uuid', video)

        if video:
            # Algo complet
            filtre = {"uuid": video, "current_user": user.uuid if user else None}
            query = f"""
                MATCH 
                {"(u:Utilisateur {uuid: $current_user})," if user else ""}
                (v:{video_class}|{playlist_class}),
                (c:{video_class}|{playlist_class}{" {uuid: $uuid}"})

                WHERE v.uuid <> c.uuid
                {"AND NOT ( (u:Utilisateur)-[:REGARDER_EXTRAITS|REGARDER_INTERVIEWS]-(v))" if user else ""}

                // Permet de compter les éléments en commun pour ordonner

                OPTIONAL MATCH (c)--{"{0,3}"}(c_t:Theme)
                OPTIONAL MATCH (v)--{"{0,3}"}(v_t:Theme)

                OPTIONAL MATCH (c)--{"{0,2}"}(c_a:Artiste)
                OPTIONAL MATCH (v)--{"{0,2}"}(v_a:Artiste)

                OPTIONAL MATCH (c)--{"{0,2}"}(c_q:Question)
                OPTIONAL MATCH (v)--{"{0,2}"}(v_q:Question)

                WITH v, c,
                collect(DISTINCT c_t) AS c_themes,
                collect(DISTINCT v_t) AS v_themes,
                collect(DISTINCT c_a) AS c_artistes,
                collect(DISTINCT v_a) AS v_artistes,
                collect(DISTINCT c_q) AS c_questions,
                collect(DISTINCT v_q) AS v_questions

                WITH v, c,
                size([t IN c_themes WHERE t IN v_themes]) AS nbThemes,
                size([a IN c_artistes WHERE a IN v_artistes]) AS nbArtistes,
                size([s IN c_questions WHERE s IN v_questions]) AS nbQuestions,
                // Champ de date non uniforme entre les extraits et les interviews
                coalesce(v.date, v.uploaded_at) AS date

                RETURN v,

                nbThemes * {poids.get('Thème', 0)} +
                nbArtistes * {poids.get('Artiste', 0)} +
                nbQuestions * {poids.get('Question', 0)}
                AS score

                ORDER BY score DESC, date DESC

                LIMIT {size}
                """
        else:
            # Recommandation de base
            filtre = {"current_user": user.uuid if user else None}
            query = f"""
                MATCH (v:{Extrait.__name__}|{Interview.__name__})
                {"OPTIONAL MATCH (u:Utilisateur {uuid: $current_user})" if user else ""}
                {"WHERE NOT ( (u)-[:REGARDER_EXTRAITS|REGARDER_INTERVIEWS]->(v) )" if user else ""}
                WITH v, coalesce(v.date, v.uploaded_at) AS date
                RETURN v, date
                ORDER BY date DESC
                LIMIT {size}
                """

        print(query, filtre)
        try:
            recommandations_cypher = db.cypher_query(query, filtre)[0]
        except ServiceUnavailable:
            raise ConnexionDB()

        # print(recommandations_cypher[0])

        # Convertir le retour de la requête CYPHER en liste d'Extrait et Interview en json
        recommandations = [
            {'value': ExtraitSerializer(Extrait.inflate(recommandation[0]), context=context).data, 'type': list(recommandation[0].labels)[0]}
            if 'Extrait' in recommandation[0].labels
            else
            {'value': InterviewSerializer(Interview.inflate(recommandation[0]), context=context).data, 'type': list(recommandation[0].labels)[0]}
            if 'Interview' in recommandation[0].labels
            else {'value':recommandation[0], 'type': list(recommandation[0].labels)[0]}
            for recommandation in recommandations_cypher
        ]

        return Response(recommandations)



def get_current_user(request):
    authorization = request.headers.get("Authorization", None)
    if authorization:
        token = authorization.split()[1]
        try:
            access = AccessToken(token)
        except ExpiredTokenError:
            raise NotAuthenticated()
        try:
            user: Utilisateur = Utilisateur.nodes.get(uuid=access["user_id"])
        except ServiceUnavailable:
            raise ConnexionDB()
        return user
    else:
        return None
