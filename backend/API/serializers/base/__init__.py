"""
Ensemble des classes Serializer contenant les méthodes génériques utilisé par leurs classes enfants
"""

from .base_serializer import BaseSerializer
from .base_relationship_serializer import BaseRelationShipSerializer
from .relationship_utilisateur_serializer import RelationShipUtilisateurSerializer
from .relationship_tag_serializer import RelationShipTagSerializer

__all__ = (
    "BaseSerializer",
    "BaseRelationShipSerializer",
    "RelationShipUtilisateurSerializer",
    "RelationShipTagSerializer",
)
