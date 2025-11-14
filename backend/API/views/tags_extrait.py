from ..views import BaseRelationShipViewSet
from ..models import Extrait, Tag
from ..serializers import TagsExtraitRelationShipSerializer

class TagsExtraitRelationShipViewSet(BaseRelationShipViewSet):
    def __init__(self, **kwargs):
        super().__init__(TagsExtraitRelationShipSerializer, Tag, 'extrait_uuid', Extrait, 'TAGS_EXTRAIT', **kwargs)
