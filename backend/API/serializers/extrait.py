from rest_framework import serializers
from neomodel.exceptions import DoesNotExist
from neomodel import db
from ..serializers import Base
from ..errors import NotFound
from ..models import Artiste, Extrait, Question


class ExtraitSerializer(Base):
    """
    Sérializer du node Extrait
    """
    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    youtube_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    vimeo_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    uploaded_at = serializers.DateField(required=False, allow_null=True)
    duree = serializers.IntegerField(required=True)

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
        super().__init__(Extrait, *args, **kwargs)
        if not self.context.get("interview"):
            self.fields.pop("position", None)

    def get_artiste(self, extrait):
        """
        Renvoie un lien propre vers l'artiste :
        """
        artiste = extrait.interviewer.single()
        return self.get_url('artiste-detail', kwargs={'uuid': artiste.uuid}) if artiste else None

    def get_question(self, extrait):
        """
        Renvoie un lien propre vers la question :
        """
        question = extrait.question.single()
        return self.get_url('question-detail', kwargs={'uuid': question.uuid}) if question else None

    def get_interviews(self, extrait):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.get_url('interview-list', kwargs={'extrait_uuid': extrait.uuid})

    def get_tags(self, extrait):
        """
        Renvoie un lien propre vers les tags :
        """
        return self.get_url('tag-list', kwargs={'extrait_uuid': extrait.uuid})
    
    def get_position(self, extrait):
        interview = self.context.get('interview')
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

        extrait = super().create(validated_data)

        if artiste_uuid:
            try:
                artiste = Artiste.nodes.get(uuid=artiste_uuid)
                extrait.interviewer.connect(artiste)
            except DoesNotExist:
                raise NotFound(Artiste)

        if question_uuid is not None:
            try:
                question_node = Question.nodes.get(uuid=question_uuid)
            except DoesNotExist:
                raise NotFound(Question)
            extrait.question.connect(question_node)

        return extrait

    def update(self, extrait, validated_data):
        """
        Modification d'un extrait
        """
        artiste_uuid = validated_data.pop("artiste_uuid", None)
        question_uuid = validated_data.pop('question_uuid', None)

        extrait = super().update(extrait, validated_data)

        # update question relation if provided
        if question_uuid is not None:
            try:
                question = Question.nodes.get(uuid=question_uuid)
            except DoesNotExist:
                raise NotFound(Question)
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
            except DoesNotExist:
                raise NotFound(Artiste)

        return extrait
