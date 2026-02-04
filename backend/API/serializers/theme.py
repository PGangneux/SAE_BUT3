from rest_framework import serializers
from ..serializers import BaseSerializer
from ..models import Theme


class ThemeSerializer(BaseSerializer):
    """
    Sérializer du node Theme
    """

    name = serializers.CharField(required=True)

    # Outputs
    questions = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Theme, *args, **kwargs)

    def get_questions(self, theme):
        """
        Renvoie un lien propre vers les questions :
        """
        return self.get_url("question-list", kwargs={"theme_uuid": theme.uuid})
