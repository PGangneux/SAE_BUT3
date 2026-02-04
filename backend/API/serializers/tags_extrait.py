from ..serializers import RelationShipTagSerializer
from ..models import Extrait


class TagsExtraitRelationShipSerializer(RelationShipTagSerializer):
    """
    Sérializer RelationShip tags_extrait (Extrait <-> Tag)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(Extrait, "tags_extrait", *args, **kwargs)
