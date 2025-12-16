from datetime import datetime
from rest_framework import serializers
from neomodel import StructuredNode, db
from ...models import Utilisateur
from ...errors import ContextError
from . import BaseRelationShipSerializer


class RelationShipUtilisateurSerializer(BaseRelationShipSerializer):
    # Outputs
    date_heure = serializers.SerializerMethodField(read_only=True)

    def __init__(self, node: StructuredNode, relationship: str, *args, **kwargs):
        super().__init__(node, Utilisateur, relationship, *args, **kwargs)

    def get_date_heure(self, instance):
        """
        Renvoie la date et l'heure :
        """
        utilisateur = self.context.get(self.context_node.__name__.lower())
        if not utilisateur:
            raise ContextError(self.context_node)
        query = (
            "MATCH (i:"
            + self.node.__name__
            + " {uuid:$uuid})<-[r:"
            + self.relationship.upper()
            + "]-(e:Utilisateur {uuid:$utilisateur}) RETURN r"
        )
        res = db.cypher_query(
            query, {"uuid": instance.uuid, "utilisateur": utilisateur.uuid}
        )[0][0]
        return datetime.fromtimestamp(res[0].get("date_heure")).isoformat()
