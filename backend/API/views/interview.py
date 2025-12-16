from ..views import BaseModelViewSet, SubBaseModelViewSet
from ..models import Interview, Tag
from ..serializers import InterviewSerializer


class InterviewViewSet(BaseModelViewSet):
    """
    Renvoie les interviews
    """

    def __init__(self, **kwargs):
        super().__init__(InterviewSerializer, Interview, "titre", **kwargs)


class TagInterviewViewSet(SubBaseModelViewSet):
    """
    Renvoie les interviews en fonction d'un tag
    """

    def __init__(self, **kwargs):
        super().__init__(
            InterviewSerializer,
            Interview,
            "tag_uuid",
            Tag,
            "TAGS_INTERVIEW",
            "titre",
            **kwargs
        )
