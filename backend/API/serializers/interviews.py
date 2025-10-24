from django.urls import reverse
from rest_framework import serializers
from neomodel import db
from ..models import Interview


class InterviewsSerializer(serializers.Serializer):
    """
    Sérializer RelationShip interviews (Extrait <-> Interview)
    """
    uuid = serializers.CharField(required=True)
    position = serializers.IntegerField(write_only=True, required=True)

    # Outputs
    titre = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    occasion = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    lieu = serializers.CharField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def get_extraits(self, interview):
        return {"url": self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'interview_uuid': interview.uuid}))}

    def get_tags(self, interview):
        return {"url": self.context.get('request').build_absolute_uri(reverse('tag-list', kwargs={'interview_uuid': interview.uuid}))}

    def create(self, validated_data):
        """Connecte une interview à un extrait"""
        extrait = self.context.get('extrait')
        if not extrait:
            raise serializers.ValidationError("Extrait manquant dans le contexte.")

        interview_uuid = validated_data['uuid']
        position = validated_data['position']
        try:
            interview = Interview.nodes.get(uuid=interview_uuid)
        except Interview.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Interview introuvable.'})

        if not extrait.interviews.is_connected(interview):
            extrait.interviews.connect(interview, {'position': position})

        return interview

    def delete(self, interview_uuid):
        """Déconnecte une inteview d’un extrait"""
        extrait = self.context.get('extrait')
        if not extrait:
            raise serializers.ValidationError("Extrait manquant dans le contexte.")

        try:
            artiste = Interview.nodes.get(uuid=interview_uuid)
        except Interview.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Interview introuvable.'})

        extrait.interviews.disconnect(artiste)
        return artiste

class PositionInputSerializer(serializers.Serializer):
    position = serializers.IntegerField(write_only=True, required=True)