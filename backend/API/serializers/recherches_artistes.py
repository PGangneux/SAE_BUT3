from datetime import datetime
from django.urls import reverse
from rest_framework import serializers
from neomodel import db
from neomodel.exceptions import DoesNotExist
from ..models import Artiste, Utilisateur
from ..errors import NotFound, ContextError


class RecherchesArtistesSerializer(serializers.Serializer):
    """
    Sérializer RelationShip recherches_artistes (Utilisateur <-> Artiste)
    """
    uuid = serializers.CharField(required=True)

    # Outputs
    date_heure = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(read_only=True)
    info = serializers.CharField(read_only=True)
    nation = serializers.SerializerMethodField(read_only=True)
    styles = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def get_date_heure(self, artiste):
        """
        Renvoie la date et l'heure :
        """
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise ContextError(Utilisateur)
        query = "MATCH (i:Artiste {uuid:$artiste})<-[r:RECHERCHES_ARTISTES]-(e:Utilisateur {uuid:$utilisateur}) RETURN r"
        res = db.cypher_query(query, {'artiste': artiste.uuid, 'utilisateur': utilisateur.uuid})[0][0]
        return datetime.fromtimestamp(res[0].get('date_heure')).isoformat()

    def get_nation(self, artiste):
        """
        Renvoie un lien propre vers la nation :
        """
        nation = artiste.nationalite.single()
        return self.context.get('request').build_absolute_uri(reverse('nation-detail', kwargs={'uuid': nation.uuid})) if nation else None 

    def get_styles(self, artiste):
        """
        Renvoie un lien propre vers les styles :
        """
        return self.context.get('request').build_absolute_uri(reverse('style-list', kwargs={'artiste_uuid': artiste.uuid}))

    def get_extraits(self, artiste):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'artiste_uuid': artiste.uuid}))

    def create(self, validated_data):
        """
        Connecte un artiste à un utilisateur
        """
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise ContextError(Utilisateur)

        artiste_uuid = validated_data['uuid']
        try:
            artiste = Artiste.nodes.get(uuid=artiste_uuid)
        except DoesNotExist:
            raise NotFound(Artiste)

        if not utilisateur.recherches_artistes.is_connected(artiste):
            utilisateur.recherches_artistes.connect(artiste)

        return artiste

    def delete(self, artiste_uuid):
        """
        Déconnecte un artiste d’un utilisateur
        """
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise ContextError(Utilisateur)

        try:
            artiste = Artiste.nodes.get(uuid=artiste_uuid)
        except DoesNotExist:
            raise NotFound(Artiste)

        utilisateur.recherches_artistes.disconnect(artiste)
        return artiste
