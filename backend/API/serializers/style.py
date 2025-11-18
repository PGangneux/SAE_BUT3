from rest_framework import serializers
from ..serializers import RelationShipBase
from ..models import Artiste, StyleMusical

class StyleRelationShipSerializer(RelationShipBase):
    """
    Sérializer RelationShip style (Artiste <-> Style)
    """
    name = serializers.CharField(read_only=True)

    # Output
    artistes = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(StyleMusical, Artiste, 'style', *args, **kwargs)

    def get_artistes(self, style_musical):
        """
        Renvoie un lien propre vers les artistes :
        """
        return self.get_url('artiste-list', kwargs={'stylemusical_uuid': style_musical.uuid})
