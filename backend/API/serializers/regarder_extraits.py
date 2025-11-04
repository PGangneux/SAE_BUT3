from datetime import datetime
from django.urls import reverse
from rest_framework import serializers
from neomodel import db
from ..models import Extrait


class RegarderExtraitsSerializer(serializers.Serializer):
    """
    Sérializer RelationShip regarder_extraits (Utilisateur <-> Extrait)
    """
    uuid = serializers.CharField(required=True)

    # Outputs
    date_heure = serializers.SerializerMethodField(read_only=True)
    titre = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    youtube_url = serializers.CharField(read_only=True)
    vimeo_url = serializers.CharField(read_only=True)
    uploaded_at = serializers.DateField(read_only=True)
    duree = serializers.IntegerField(read_only=True)
    artiste = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)
    interviews = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def get_date_heure(self, extrait):
        """
        Renvoie la date et l'heure :
        """
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise serializers.ValidationError("Utilisateur manquant dans le contexte.")
        query = "MATCH (i:Extrait {uuid:$extrait})<-[r:REGARDER_EXTRAITS]-(e:Utilisateur {uuid:$utilisateur}) RETURN r"
        res = db.cypher_query(query, {'extrait': extrait.uuid, 'utilisateur': utilisateur.uuid})[0][0]
        return datetime.fromtimestamp(res[0].get('date_heure')).isoformat()

    def get_artiste(self, extrait):
        """
        Renvoie un lien propre vers l'artiste :
        """
        artiste = extrait.interviewer.single()
        return self.context.get('request').build_absolute_uri(reverse('artiste-detail', kwargs={'uuid': artiste.uuid})) if artiste else None

    def get_question(self, extrait):
        """
        Renvoie un lien propre vers la question :
        """
        question = extrait.question.single()
        return self.context.get('request').build_absolute_uri(reverse('question-detail', kwargs={'uuid': question.uuid})) if question else None

    def get_interviews(self, extrait):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.context.get('request').build_absolute_uri(reverse('interview-list', kwargs={'extrait_uuid': extrait.uuid}))

    def get_tags(self, extrait):
        """
        Renvoie un lien propre vers les tags :
        """
        return self.context.get('request').build_absolute_uri(reverse('tag-list', kwargs={'extrait_uuid': extrait.uuid}))

    def create(self, validated_data):
        """
        Connecte un extrait à un utilisateur
        """
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise serializers.ValidationError("Utilisateur manquant dans le contexte.")

        extrait_uuid = validated_data['uuid']
        try:
            extrait = Extrait.nodes.get(uuid=extrait_uuid)
        except Extrait.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Extrait introuvable.'})

        if not utilisateur.regarder_extraits.is_connected(extrait):
            utilisateur.regarder_extraits.connect(extrait)

        return extrait

    def delete(self, extrait_uuid):
        """
        Déconnecte un extrait d’un utilisateur
        """
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise serializers.ValidationError("Utilisateur manquant dans le contexte.")

        try:
            extrait = Extrait.nodes.get(uuid=extrait_uuid)
        except Extrait.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Extrait introuvable.'})

        utilisateur.regarder_extraits.disconnect(extrait)
        return extrait
