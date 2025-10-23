from datetime import datetime
from django.urls import reverse
from rest_framework import serializers
from neomodel import db
from ..models import Artiste


class RecherchesArtistesSerializer(serializers.Serializer):
    uuid = serializers.CharField(required=True)

    # Outputs
    date_heure = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(read_only=True)
    info = serializers.CharField(read_only=True)
    styles = serializers.SerializerMethodField(read_only=True)
    nation = serializers.SerializerMethodField(read_only=True)
    interviews = serializers.SerializerMethodField(read_only=True)

    def get_date_heure(self, artiste):
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise serializers.ValidationError("Utilisateur manquant dans le contexte.")
        query = "MATCH (i:Artiste {uuid:$artiste})<-[r:RECHERCHES_ARTISTES]-(e:Utilisateur {uuid:$utilisateur}) RETURN r"
        res = db.cypher_query(query, {'artiste': artiste.uuid, 'utilisateur': utilisateur.uuid})[0][0]
        return datetime.fromtimestamp(res[0].get('date_heure')).isoformat()

    def get_styles(self, artiste):
        return {"url": self.context.get('request').build_absolute_uri(reverse('style-list', kwargs={'artiste_uuid': artiste.uuid}))}
    
    def get_nation(self, artiste):
        if artiste.nationalite:
            return {"url": self.context.get('request').build_absolute_uri(reverse('nation-detail', kwargs={'uuid': artiste.nationalite.single().uuid}))}
        return None

    def get_interviews(self, artiste):
        return {"url": self.context.get('request').build_absolute_uri(reverse('interview-list', kwargs={'artiste_uuid': artiste.uuid}))}

    def create(self, validated_data):
        """Connecte un artiste à un utilisateur"""
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise serializers.ValidationError("Utilisateur manquant dans le contexte.")

        artiste_uuid = validated_data['uuid']
        try:
            artiste = Artiste.nodes.get(uuid=artiste_uuid)
        except Artiste.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Artiste introuvable.'})

        if not utilisateur.recherches_artistes.is_connected(artiste):
            utilisateur.recherches_artistes.connect(artiste)

        return artiste

    def delete(self, artiste_uuid):
        """Déconnecte un artiste d’un utilisateur"""
        utilisateur = self.context.get('utilisateur')
        if not utilisateur:
            raise serializers.ValidationError("Utilisateur manquant dans le contexte.")

        try:
            artiste = Artiste.nodes.get(uuid=artiste_uuid)
        except Artiste.DoesNotExist:
            raise serializers.ValidationError({'uuid': 'Artiste introuvable.'})

        utilisateur.recherches_artistes.disconnect(artiste)
        return artiste
