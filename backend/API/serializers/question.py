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
    input_fields = {"theme_uuid": {"relationship": "theme", "node": Theme}}
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
