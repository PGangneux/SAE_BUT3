from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from ..models import Utilisateur


class UtilisateurSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    pseudo = serializers.CharField(required=True)
    prenom = serializers.CharField(required=True)
    nom = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    is_admin = serializers.BooleanField()

    # # optional relationships creation via serializer (lists of dicts with uuid + date_heure)
    # recherches_artistes = serializers.ListField(
    #     child=serializers.DictField(), write_only=True, required=False,
    #     help_text="Liste d'objets {'uuid': artiste_uuid, 'date_heure': ISO_datetime}"
    # )
    # watched_interviews = serializers.ListField(
    #     child=serializers.DictField(), write_only=True, required=False
    # )
    # watched_extraits = serializers.ListField(
    #     child=serializers.DictField(), write_only=True, required=False
    # )
    # searched_questions = serializers.ListField(
    #     child=serializers.DictField(), write_only=True, required=False
    # )

    def create(self, validated_data):
        # handle relations lists separately
        # recherches = validated_data.pop('recherches_artistes', [])
        # watched_i = validated_data.pop('watched_interviews', [])
        # watched_e = validated_data.pop('watched_extraits', [])
        # searched_q = validated_data.pop('searched_questions', [])

        # hash password
        raw_pwd = validated_data.pop('password')
        validated_data['password'] = make_password(raw_pwd)

        user = Utilisateur(**validated_data).save()

        # # helper to connect relations with date_heure
        # def connect_rel_list(rel_name, target_cls, items):
        #     for item in items:
        #         uuid = item.get('uuid')
        #         date_heure = item.get('date_heure')
        #         if not uuid or not date_heure:
        #             raise serializers.ValidationError({rel_name: 'Chaque élément nécessite uuid et date_heure.'})
        #         try:
        #             target = target_cls.nodes.get(uuid=uuid)
        #         except DoesNotExist:
        #             raise serializers.ValidationError({rel_name: f'Target introuvable: {uuid}'})
        #         rel = getattr(user, rel_name)
        #         # connect avec la propriété date_heure
        #         rel.connect(target, {'date_heure': date_heure})

        # connect_rel_list('recherches_artistes', Artiste, recherches)
        # connect_rel_list('watched_interviews', Interview, watched_i)
        # connect_rel_list('watched_extraits', Extrait, watched_e)
        # connect_rel_list('searched_questions', Question, searched_q)

        return user

    def update(self, instance, validated_data):
        # mise à jour simple des champs et du mot de passe si fourni
        pwd = validated_data.pop('password', None)
        if pwd:
            instance.password = make_password(pwd)

        # update direct properties
        for k, v in validated_data.items():
            # # ignore relations handled separately in this method
            # if k in ('recherches_artistes', 'watched_interviews', 'watched_extraits', 'searched_questions'):
            #     continue
            setattr(instance, k, v)
        instance.save()
        return instance