from django.urls import reverse
from rest_framework import serializers
from neomodel.exceptions import DoesNotExist
from neomodel import db
from ..models import Artiste, Extrait, Question


class ExtraitSerializer(serializers.Serializer):
    """
    Sérializer du node Extrait
    """
    uuid = serializers.CharField(read_only=True)
    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    youtube_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    vimeo_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    uploaded_at = serializers.DateField(required=False, allow_null=True)

    # Input:
    artiste_uuid = serializers.CharField(write_only=True, required=False)
    question_uuid = serializers.CharField(write_only=True, required=False)

    # Output:
    artiste = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)
    interviews = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    position = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """Retire le champ `position` si aucune interview n'est dans le contexte."""
        super().__init__(*args, **kwargs)
        if not self.context.get("interview"):
            self.fields.pop("position", None)

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
    
    def get_position(self, extrait):
        interview = self.context.get('interview')
        if not interview:
            return None
        return int(db.cypher_query(
            "MATCH (e:Extrait {uuid:$extrait_uuid})-[r:APPARTIENT_A]->(i:Interview {uuid:$interview_uuid}) RETURN r.position AS pos",
            {'extrait_uuid': extrait.uuid, 'interview_uuid': interview.uuid}
        )[0][0][0])

    def create(self, validated_data):
        """
        Création d'un extrait
        """
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
        """
        Modification d'un extrait
        """
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
