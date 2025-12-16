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

    def get(self, request: HttpRequest) -> Response:
        return self.post(request)

    def post(self, request: HttpRequest) -> Response:
        data: dict = request.data
        poids = data.get("weights", False)
        print("poids:", poids)
        filtres = data.get("filters", False)
        print("filtres:", filtres)

        user = get_current_user(request)
        print("user: ", user.pseudo if user else None)

        context = {"request": request}

        video = request.GET.get("video", False)
        size: str = request.GET.get("size", "10")
        if size.isnumeric():
            try:
                size: int = int(size)
            except:
                raise ValidationError(detail="{size: numeric not string}")

        # Modulabilité du modèle
        video_class = Extrait.__name__
        playlist_class = Interview.__name__

        print("uuid", video)

        # Algo complet
        query = f"""
            MATCH 

            // Si utilisateur est connecté
            {"(u:Utilisateur {uuid: $current_user})," if user else ""}

            // Si la vidéo cliqué est fourni
            {f"(c:{video_class}|{playlist_class}{" {uuid: $uuid}"})," if video else ""}

            // La vidéo (Extrait / Interview ) que l'on veut recommander
            (v:{video_class}|{playlist_class})

            // Conditions
            WHERE True
            // Que la vidéo recommandé ne soit pas celle actuellement visionner
            {"AND v.uuid <> c.uuid" if video else ""}
            // Si utilisateur connecté, on retire les vidéos déjà regarder (TODO les mettre en derniers)
            {"AND NOT ( (u:Utilisateur)-[:REGARDER_EXTRAITS|REGARDER_INTERVIEWS]-(v))" if user else ""}

            // Filtres
            // Filtre par Thème
            {
                f"""AND EXISTS {"{ MATCH p = SHORTEST 1 (v)-[*2..3]-(t:Theme) WHERE t.uuid = "}'{filtres.get("Thème")}'
                {
                    """
                    AND NONE(n IN nodes(p) WHERE n:Utilisateur)
                    AND NONE(r IN relationships(p) WHERE type(r) IN ['REGARDER_EXTRAITS','REGARDER_INTERVIEWS','RECHERCHES_ARTISTES','RECHERCHES_QUESTIONS']) }
                    """
                }
                """
                if filtres and filtres.get('Thème', False) else ""
            }

            // Filtre par Artiste
            {
                f"""AND EXISTS {"{ MATCH p = SHORTEST 1 (v)-[*..2]-(a:Artiste) WHERE a.uuid = "}'{filtres.get("Artiste")}'
                {
                    """
                    AND NONE(n IN nodes(p) WHERE n:Utilisateur)
                    AND NONE(r IN relationships(p) WHERE type(r) IN ['REGARDER_EXTRAITS','REGARDER_INTERVIEWS','RECHERCHES_ARTISTES','RECHERCHES_QUESTIONS']) }
                    """
                }
                """
                if filtres and filtres.get('Artiste', False) else ""
            }

            // Filtre par Style Musical
            {
                f"""AND EXISTS {"{ MATCH p = SHORTEST 1 (v)-[*2..3]-(s:StyleMusical) WHERE s.uuid = "}'{filtres.get("StyleMusical")}'
                {
                    """
                    AND NONE(n IN nodes(p) WHERE n:Utilisateur)
                    AND NONE(r IN relationships(p) WHERE type(r) IN ['REGARDER_EXTRAITS','REGARDER_INTERVIEWS','RECHERCHES_ARTISTES','RECHERCHES_QUESTIONS']) }
                    """
                }
                """
                if filtres and filtres.get('StyleMusical', False) else ""
            }

            // Filtre par Nation
            {
                f"""AND EXISTS {"{ MATCH p = SHORTEST 1 (v)-[*2..3]-(n:Nation) WHERE n.uuid = "}'{filtres.get("Nation")}'
                {
                    """
                    AND NONE(n IN nodes(p) WHERE n:Utilisateur)
                    AND NONE(r IN relationships(p) WHERE type(r) IN ['REGARDER_EXTRAITS','REGARDER_INTERVIEWS','RECHERCHES_ARTISTES','RECHERCHES_QUESTIONS']) }
                    """
                }
                """
                if filtres and filtres.get('Nation', False) else ""
            }

            // Filtre par Question
            {
                f"""
                AND EXISTS {"{ MATCH p = SHORTEST 1 (v)-[*..2]-(q:Question) WHERE q.uuid = "}'{filtres.get("Question")}'
                {
                    """
                    AND NONE(n IN nodes(p) WHERE n:Utilisateur)
                    AND NONE(r IN relationships(p) WHERE type(r) IN ['REGARDER_EXTRAITS','REGARDER_INTERVIEWS','RECHERCHES_ARTISTES','RECHERCHES_QUESTIONS']) }
                    """
                }
                """
                if filtres and filtres.get('Question', False) else ""
            }

            // Filtre par Tag
            {
                f"""
                AND EXISTS {"{ MATCH p = SHORTEST 1 (v)-[*0..3]-(!:Tag) WHERE !.uuid = "}'{filtres.get("Tag")}'
                {
                    """
                    AND NONE(n IN nodes(p) WHERE n:Utilisateur)
                    AND NONE(r IN relationships(p) WHERE type(r) IN ['REGARDER_EXTRAITS','REGARDER_INTERVIEWS','RECHERCHES_ARTISTES','RECHERCHES_QUESTIONS']) }
                    """
                }
                """
                if filtres and filtres.get('Tag', False) else ""
            }

            // Permet de compter les éléments en commun pour ordonner
            // Récupère les thèmes des vidéos
            {
                "OPTIONAL MATCH (c)-[*0..3]-(c_t:Theme) OPTIONAL MATCH (v)-[*0..3]-(v_t:Theme)"
                if poids and poids.get('Thème', False) and video else ""
            }

            // Récupère les artistes des vidéos
            {
                "OPTIONAL MATCH (c)-[*0..2]-(c_a:Artiste) OPTIONAL MATCH (v)-[*0..2]-(v_a:Artiste)"
                if poids and poids.get('Artiste', False) and video else ""
            }

            // Récupère les questions des vidéos
            {
                "OPTIONAL MATCH (c)-[*0..2]-(c_q:Question) OPTIONAL MATCH (v)-[*0..2]-(v_q:Question)"
                if poids and poids.get('Question', False) and video else ""
            }

            // Liste
            WITH {"c," if video else ""}
            // Liste les thèmes des vidéos
            {"collect(DISTINCT c_t) AS c_themes, collect(DISTINCT v_t) AS v_themes," if poids and poids.get('Thème', False) and video else ""}

            // Liste les artistes des vidéos
            {"collect(DISTINCT c_a) AS c_artistes, collect(DISTINCT v_a) AS v_artistes," if poids and poids.get('Artiste', False) and video else ""}
            
            // Liste les questions des vidéos
            {"collect(DISTINCT c_q) AS c_questions, collect(DISTINCT v_q) AS v_questions," if poids and poids.get('Question', False) and video else ""}
            v

            // Compte
            WITH {"c," if video else ""}

            // Compte le nombre de thèmes
            {"size([t IN c_themes WHERE t IN v_themes]) AS nbThemes," if poids and poids.get('Thème') and video else ""}

            // Compte le nombre d'artistes
            {"size([a IN c_artistes WHERE a IN v_artistes]) AS nbArtistes," if poids and poids.get('Artiste') and video else ""}

            // Compte le nombre de questions
            {"size([s IN c_questions WHERE s IN v_questions]) AS nbQuestions," if poids and poids.get('Question') and video else ""}

            // Champ de date non uniforme entre les extraits et les interviews
            v, coalesce(v.date, v.uploaded_at) AS date
            
            // Ce que l'on renvoi à la fin de la requête CYPHER
            RETURN v,

            // Création du score en fonction des weights
            {f"nbThemes * {poids.get('Thème')} +" if poids and poids.get('Thème', False) and video else ""}
            {f"nbArtistes * {poids.get('Artiste')} +" if poids and poids.get('Artiste', False) and video else ""}
            {f"nbQuestions * {poids.get('Question')} +" if poids and poids.get('Question', False) and video else ""}
            0 // Pour ne pas avoir de '+' dans le vide
            AS score

            // On ordonne par score puis par date et enfin de l'aléatoire
            ORDER BY score DESC, date DESC, rand() DESC

            // Le nombre de vidéo à renvoyer
            LIMIT $size
            """
        filtre = {
            "uuid": video,
            "current_user": user.uuid if user else None,
            "size": size,
        }
        print(query, filtre)
        try:
            recommandations_cypher = db.cypher_query(query, filtre)[0]
        except ServiceUnavailable:
            raise ConnexionDB()

        # print(recommandations_cypher[0])

        # Convertir le retour de la requête CYPHER en liste d'Extrait et Interview en json
        recommandations = [
            (
                {
                    "value": ExtraitSerializer(
                        Extrait.inflate(recommandation[0]), context=context
                    ).data,
                    "type": list(recommandation[0].labels)[0],
                }
                if "Extrait" in recommandation[0].labels
                else (
                    {
                        "value": InterviewSerializer(
                            Interview.inflate(recommandation[0]), context=context
                        ).data,
                        "type": list(recommandation[0].labels)[0],
                    }
                    if "Interview" in recommandation[0].labels
                    else {
                        "value": recommandation[0],
                        "type": list(recommandation[0].labels)[0],
                    }
                )
            )
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
