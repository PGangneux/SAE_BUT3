from rest_framework import serializers
from ..serializers import Base
from ..models import StyleMusical


class StyleMusicalSerializer(Base):
    """
    Sérializer du node Style Musical
    """
    name = serializers.CharField(required=True)

    # Output
    artistes = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(StyleMusical, *args, **kwargs)

    def get_artistes(self, style_musical):
        """
        Renvoie un lien propre vers les artistes :
        """
        return self.get_url('artiste-list', kwargs={'stylemusical_uuid': style_musical.uuid})
