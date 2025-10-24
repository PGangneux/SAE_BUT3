from django.urls import reverse
from rest_framework import serializers
from ..models import Interview


class InterviewSerializer(serializers.Serializer):
    """
    Sérializer du node Interview
    """
    uuid = serializers.CharField(read_only=True)
    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date = serializers.DateField(required=False, allow_null=True)
    occasion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lieu = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Outputs
    extraits = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def get_extraits(self, interview):
        """
        Renvoie un lien propre vers les extraits :
        """
        return {"url": self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'interview_uuid': interview.uuid}))}

    def get_tags(self, interview):
        """
        Renvoie un lien propre vers les tags :
        """
        return {"url": self.context.get('request').build_absolute_uri(reverse('tag-list', kwargs={'interview_uuid': interview.uuid}))}

    def create(self, validated_data):
        """
        Création d'une interview
        """
        return Interview(**validated_data).save()

    def update(self, instance, validated_data):
        """
        Modification d'une interview
        """
        for k, v in validated_data.items():
            setattr(instance, k, v)
        return instance.save()
