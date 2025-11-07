from datetime import datetime
from django.urls import reverse
from rest_framework import serializers
from neomodel import db
from ..models import Interview, Utilisateur
from ..errors import NotFound, ContextError
from neomodel.exceptions import DoesNotExist


class RegarderInterviewsSerializer(serializers.Serializer):
    """
    Sérializer RelationShip regarder_interviews (Utilisateur <-> Interview)
    """
    uuid = serializers.CharField(required=True)

    # Outputs
    date_heure = serializers.SerializerMethodField(read_only=True)
    titre = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    occasion = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    lieu = serializers.CharField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def get_date_heure(self, interview):
        """
        Renvoie la date et l'heure :
        """
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise ContextError(Utilisateur)
        query = "MATCH (i:Interview {uuid:$interview})<-[r:REGARDER_INTERVIEWS]-(e:Utilisateur {uuid:$utilisateur}) RETURN r"
        res = db.cypher_query(query, {'interview': interview.uuid, 'utilisateur': utilisateur.uuid})[0][0]
        return datetime.fromtimestamp(res[0].get('date_heure')).isoformat()

    def get_extraits(self, interview):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'interview_uuid': interview.uuid}))

    def get_tags(self, interview):
        """
        Renvoie un lien propre vers les tags :
        """
        return self.context.get('request').build_absolute_uri(reverse('tag-list', kwargs={'interview_uuid': interview.uuid}))

    def create(self, validated_data):
        """
        Connecte une interview à un utilisateur
        """
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise ContextError(Utilisateur)

        interview_uuid = validated_data['uuid']
        try:
            interview = Interview.nodes.get(uuid=interview_uuid)
        except DoesNotExist:
            raise NotFound(Interview)

        if not utilisateur.regarder_interviews.is_connected(interview):
            utilisateur.regarder_interviews.connect(interview)

        return interview

    def delete(self, interview_uuid):
        """
        Déconnecte une inteview d’un utilisateur
        """
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise ContextError(Utilisateur)

        try:
            artiste = Interview.nodes.get(uuid=interview_uuid)
        except DoesNotExist:
            raise NotFound(Interview)

        utilisateur.regarder_interviews.disconnect(artiste)
        return artiste
