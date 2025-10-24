from django.urls import reverse
from rest_framework import serializers
from neomodel.exceptions import DoesNotExist
from neomodel import db
from ..models import Artiste, Extrait, Question


class ExtraitSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    youtube_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    vimeo_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    uploaded_at = serializers.DateField(required=False, allow_null=True)

    # Input:
    question_uuid = serializers.CharField(write_only=True, required=False)
    artiste_uuid = serializers.CharField(write_only=True, required=False)

    # Output:
    artiste = serializers.SerializerMethodField(read_only=True)
    interviews = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def get_artiste(self, extrait):
        if extrait.interviewer:
            return {"url": self.context.get('request').build_absolute_uri(reverse('artiste-detail', kwargs={'uuid': extrait.interviewer.single().uuid}))}
        return None

    def get_interviews(self, extrait):
        return {"url": self.context.get('request').build_absolute_uri(reverse('interview-list', kwargs={'extrait_uuid': extrait.uuid}))}

    def get_tags(self, extrait):
        return {"url": self.context.get('request').build_absolute_uri(reverse('tag-list', kwargs={'extrait_uuid': extrait.uuid}))}

    def get_question(self, extrait):
        question = extrait.question.single()
        if question:
            return question.uuid
        return None

    def create(self, validated_data):
        artiste_uuid = validated_data.pop("artiste_uuid", None)
        question_uuid = validated_data.pop('question_uuid', None)

        extrait = Extrait(**validated_data).save()

        if artiste_uuid:
            try:
                artiste = Artiste.nodes.get(uuid=artiste_uuid)
                extrait.interviewer.connect(artiste)
            except Artiste.DoesNotExist:
                raise serializers.ValidationError({"artiste_uuid": "Artiste introuvable."}, 404)

        if question_uuid is not None:
            try:
                question_node = Question.nodes.get(uuid=question_uuid)
            except DoesNotExist:
                raise serializers.ValidationError({'question_uuid': 'Question introuvable.'}, 404)
            extrait.question.connect(question_node)

        return extrait

    def update(self, extrait, validated_data):
        artiste_uuid = validated_data.pop("artiste_uuid", None)
        question_uuid = validated_data.pop('question_uuid', None)

        # update props
        for k, v in validated_data.items():
            setattr(extrait, k, v)
        extrait.save()

        # update question relation if provided
        if question_uuid is not None:
            try:
                question = Question.nodes.get(uuid=question_uuid)
            except DoesNotExist:
                raise serializers.ValidationError({'question_uuid': 'Question introuvable.'})
            try:
                extrait.question.disconnect(extrait.question.single())
            except Exception:
                pass
            extrait.question.connect(question)
        
        if artiste_uuid is not None:
            try:
                if extrait.interviewer:
                    extrait.interviewer.disconnect(extrait.interviewer.single())
                if artiste_uuid:
                    extrait.interviewer.connect(Artiste.nodes.get(uuid=artiste_uuid))
            except Artiste.DoesNotExist:
                raise serializers.ValidationError({"artiste_uuid": "Artiste introuvable."}, 404)

        return extrait
