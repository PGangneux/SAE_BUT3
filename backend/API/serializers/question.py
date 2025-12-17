from rest_framework import serializers
from neomodel.exceptions import DoesNotExist
from ..serializers import BaseSerializer
from ..models import Question, Theme
from ..errors import NotFound


class QuestionSerializer(BaseSerializer):
    """
    Sérializer du node Question
    """

    texte = serializers.CharField(required=True)

    # Inputs
    theme_uuid = serializers.CharField(write_only=True, required=False)

    # Outputs
    theme = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Question, *args, **kwargs)

    def get_theme(self, question):
        """
        Renvoie un lien propre vers le theme :
        """
        theme = question.theme.single()
        return (
            self.get_url("theme-detail", kwargs={"uuid": theme.uuid}) if theme else None
        )

    def get_extraits(self, question):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url("extrait-list", kwargs={"question_uuid": question.uuid})

    def create(self, validated_data):
        """
        Création d'une question
        """
        theme_uuid = validated_data.pop("theme_uuid", None)
        question = super().create(validated_data)
        if theme_uuid:
            try:
                theme = Theme.nodes.get(uuid=theme_uuid)
                question.theme.connect(theme)
            except DoesNotExist:
                raise NotFound(Theme)
        return question

    def update(self, question, validated_data):
        """
        Modification d'une question
        """
        theme_uuid = validated_data.pop("theme_uuid", None)
        question = super().update(question, validated_data)
        try:
            theme = question.theme.single()
            if theme:
                question.theme.disconnect(theme)
            if theme_uuid:
                question.theme.connect(Theme.nodes.get(uuid=theme_uuid))
        except DoesNotExist:
            raise NotFound(Theme)
        return question
