from ..serializers import RelationShipTag
from ..models import Extrait

class TagsExtraitRelationShipSerializer(RelationShipTag):
    """
    Sérializer RelationShip tags_extrait (Extrait <-> Tag)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(Extrait, 'tags_extrait', *args, **kwargs)
