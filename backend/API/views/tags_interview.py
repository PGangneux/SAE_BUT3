from ..views import BaseRelationShipViewSet
from ..models import Interview, Tag
from ..serializers import TagsInterviewRelationShipSerializer


class TagsInterviewRelationShipViewSet(BaseRelationShipViewSet):
    def __init__(self, **kwargs):
        super().__init__(
            TagsInterviewRelationShipSerializer,
            Tag,
            "interview_uuid",
            Interview,
            "TAGS_INTERVIEW",
            **kwargs
        )
