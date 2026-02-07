from ..serializers import RelationShipTagSerializer
from ..models import Interview


class TagsInterviewRelationShipSerializer(RelationShipTagSerializer):
    """
    Sérializer RelationShip tags_interview (Interview <-> Tag)

    Gestion des tags liés à une interview
    """

    def __init__(self, *args, **kwargs):
        """
        node : Tag
        context_node : Interview
        relation : tags_interview
        """
        super().__init__(Interview, "tags_interview", *args, **kwargs)
