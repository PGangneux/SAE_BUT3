from django.urls import reverse
from rest_framework import serializers
from ..models import Artiste, Interview


class InterviewSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date = serializers.DateField(required=False, allow_null=True)
    occasion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lieu = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # relations input: lier un artiste à l'interview
    artiste_uuid = serializers.CharField(write_only=True, required=False)

    # relations output: extraits ordonnés
    artiste = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def get_artiste(self, interview):
        if interview.interviewer:
            return {"url": self.context.get('request').build_absolute_uri(reverse('artiste-detail', kwargs={'uuid': interview.interviewer.single().uuid}))}
        return None

    def get_extraits(self, interview):
        return {"url": self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'interview_uuid': interview.uuid}))}

    def get_tags(self, interview):
        return {"url": self.context.get('request').build_absolute_uri(reverse('tag-list', kwargs={'interview_uuid': interview.uuid}))}

    def create(self, validated_data):
        artiste_uuid = validated_data.pop("artiste_uuid", None)
        interview = Interview(**validated_data).save()
        if artiste_uuid:
            try:
                artiste = Artiste.nodes.get(uuid=artiste_uuid)
                interview.interviewer.connect(artiste)
            except Artiste.DoesNotExist:
                raise serializers.ValidationError({"artiste_uuid": "Artiste introuvable."}, 404)
        return interview

    def update(self, instance, validated_data):
        artiste_uuid = validated_data.pop("artiste_uuid", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        try:
            if instance.interviewer:
                instance.interviewer.disconnect(instance.interviewer.single())
            if artiste_uuid:
                instance.interviewer.connect(Artiste.nodes.get(uuid=artiste_uuid))
        except Artiste.DoesNotExist:
            raise serializers.ValidationError({"artiste_uuid": "Artiste introuvable."}, 404)
        return instance
