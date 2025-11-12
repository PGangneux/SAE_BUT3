from rest_framework import serializers
from ..serializers import Base
from ..models import Theme


class ThemeSerializer(Base):
    """
    Sérializer du node Theme
    """
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Outputs
    questions = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Theme, *args, **kwargs)

    def get_questions(self, theme):
        """
        Renvoie un lien propre vers les questions :
        """
        return self.get_url('question-list', kwargs={'theme_uuid': theme.uuid})

    def create(self, validated_data):
        """
        Création d'un theme
        """
        return super().create(validated_data)

    def update(self, theme, validated_data):
        """
        Modification d'un theme
        """
        return super().update(theme, validated_data)
