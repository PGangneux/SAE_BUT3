from ..serializers import RelationShipTag
from ..models import Interview

class TagsInterviewRelationShipSerializer(RelationShipTag):
    """
    Sérializer RelationShip tags_interview (Interview <-> Tag)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(Interview, 'tags_interview', *args, **kwargs)
