from django.urls import reverse
from rest_framework import serializers
from .models import (
    Artiste, Interview, Extrait, Question, Theme, Utilisateur
)
from django.contrib.auth.hashers import make_password
from neomodel import db
from neomodel.exceptions import DoesNotExist, UniqueProperty

class ThemeSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    questions = serializers.SerializerMethodField(read_only=True)

    def get_questions(self, theme):
        """
        Renvoie un lien propre vers les questions :
        """
        return self.context.get('request').build_absolute_uri(reverse('question-list', kwargs={'theme_uuid': theme.uuid}))

    def create(self, validated_data):
        try:
            return Theme(**validated_data).save()
        except UniqueProperty:
            raise serializers.ValidationError({"name": "Ce nom de thème existe déjà."}, 400)

    def update(self, instance: Theme, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        try:
            instance.save()
        except UniqueProperty:
            raise serializers.ValidationError({"name": "Ce nom de thème existe déjà."}, 400)
        return instance


class QuestionSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    texte = serializers.CharField(required=True)
    choices = [(None, '-----')]
    choices.extend ([(t.uuid, t.name) for t in Theme.nodes.all()])
    theme = serializers.SerializerMethodField(read_only=True)
    theme_uuid = serializers.ChoiceField(
        choices = choices,
        required=False,
        write_only=True
    )

    def get_theme(self, question):
        """
        Renvoie un lien propre vers le thème : {uuid, nom}
        """
        if question.theme:
            # Full url : 
            return self.context.get('request').build_absolute_uri(reverse('theme-detail', kwargs={'uuid': question.theme.single().uuid}))
            # Partial url : 
            # return reverse('theme-detail', kwargs={'uuid': question.theme.single().uuid})
        return None

    def create(self, validated_data):
        theme_uuid = validated_data.pop("theme_uuid", None)
        try:
            question = Question(**validated_data).save()
        except UniqueProperty:
            raise serializers.ValidationError({"text": "Cette question existe déjà"}, 400)
        if theme_uuid:
            try:
                theme = Theme.nodes.get(uuid=theme_uuid)
                question.theme.connect(theme)
            except Theme.DoesNotExist:
                raise serializers.ValidationError({"theme_uuid": "Thème introuvable."})
        return question

    def update(self, instance, validated_data):
        theme_uuid = validated_data.pop("theme_uuid", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        try:
            instance.save()
        except UniqueProperty:
            raise serializers.ValidationError({"name": "Cette question existe déjà."}, 400)
        try:
            for old in instance.theme.all():
                instance.theme.disconnect(old)
            if theme_uuid:
                instance.theme.connect(Theme.nodes.get(uuid=theme_uuid))
        except Theme.DoesNotExist:
            raise serializers.ValidationError({"theme_uuid": "Thème introuvable."}, 400)
        return instance


# class ExtraitSerializer(serializers.Serializer):
#     uuid = serializers.CharField(read_only=True)
#     titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     metadonnees = serializers.JSONField(required=False, allow_null=True)

#     youtube_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     vimeo_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     uploaded_at = serializers.DateTimeField(required=False, allow_null=True)

#     # relations input:
#     interview_uuid = serializers.CharField(write_only=True, required=False)
#     position = serializers.IntegerField(write_only=True, required=False)
#     question_uuid = serializers.CharField(write_only=True, required=False)

#     # relations output:
#     interview = serializers.SerializerMethodField(read_only=True)
#     question = serializers.SerializerMethodField(read_only=True)

#     def get_interview(self, obj):
#         try:
#             # obj.interview is RelationshipTo; get single connected node if exists
#             interviews = obj.interview.all()
#             if interviews:
#                 # récupérer relation properties via cypher
#                 q = """
#                 MATCH (i:Interview {uuid:$iid})<-[r:APPARTIENT_A]-(e:Extrait {uuid:$eid})
#                 RETURN i, r
#                 """
#                 res, _ = db.cypher_query(q, {'iid': interviews[0].uuid, 'eid': obj.uuid})
#                 if res:
#                     node_props = res[0][0]
#                     rel_props = res[0][1]
#                     return {
#                         'uuid': node_props.get('uuid'),
#                         'titre': node_props.get('titre'),
#                         'position': rel_props.get('position')
#                     }
#                 return {'uuid': interviews[0].uuid, 'titre': interviews[0].titre}
#         except Exception:
#             pass
#         return None

#     def get_question(self, obj):
#         try:
#             qn = obj.question.all()
#             if qn:
#                 return {'uuid': qn[0].uuid, 'texte': qn[0].texte}
#         except Exception:
#             pass
#         return None

#     def validate(self, data):
#         # si interview_uuid fourni, position doit aussi l'être
#         if 'interview_uuid' in data and 'position' not in data:
#             raise serializers.ValidationError({
#                 'position': 'Le champ position est requis quand interview_uuid est fourni.'
#             })
#         return data

#     def create(self, validated_data):
#         interview_uuid = validated_data.pop('interview_uuid', None)
#         position = validated_data.pop('position', None)
#         question_uuid = validated_data.pop('question_uuid', None)

#         extrait = Extrait.nodes.create(**{k: v for k, v in validated_data.items() if v is not None})

#         if interview_uuid is not None:
#             try:
#                 interview_node = Interview.nodes.get(uuid=interview_uuid)
#             except DoesNotExist:
#                 raise serializers.ValidationError({'interview_uuid': 'Interview introuvable.'})
#             # connecter avec propriété position
#             extrait.interview.connect(interview_node, {'position': position})

#         if question_uuid is not None:
#             try:
#                 question_node = Question.nodes.get(uuid=question_uuid)
#             except DoesNotExist:
#                 raise serializers.ValidationError({'question_uuid': 'Question introuvable.'})
#             extrait.question.connect(question_node)

#         return extrait

#     def update(self, instance, validated_data):
#         interview_uuid = validated_data.pop('interview_uuid', None)
#         position = validated_data.pop('position', None)
#         question_uuid = validated_data.pop('question_uuid', None)

#         # update props
#         for k, v in validated_data.items():
#             setattr(instance, k, v)
#         instance.save()

#         # update interview relation if provided
#         if interview_uuid is not None:
#             try:
#                 interview_node = Interview.nodes.get(uuid=interview_uuid)
#             except DoesNotExist:
#                 raise serializers.ValidationError({'interview_uuid': 'Interview introuvable.'})
#             # Disconnect existing interview relations then connect new with position
#             try:
#                 for old in instance.interview.all():
#                     instance.interview.disconnect(old)
#             except Exception:
#                 pass
#             instance.interview.connect(interview_node, {'position': position})

#         # update question relation if provided
#         if question_uuid is not None:
#             try:
#                 question_node = Question.nodes.get(uuid=question_uuid)
#             except DoesNotExist:
#                 raise serializers.ValidationError({'question_uuid': 'Question introuvable.'})
#             try:
#                 for old in instance.question.all():
#                     instance.question.disconnect(old)
#             except Exception:
#                 pass
#             instance.question.connect(question_node)

#         return instance


# class InterviewSerializer(serializers.Serializer):
#     uuid = serializers.CharField(read_only=True)
#     titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     date = serializers.DateField(required=False, allow_null=True)
#     occasion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     lieu = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     metadonnees = serializers.JSONField(required=False, allow_null=True)

#     # relations input: lier un artiste à l'interview
#     artiste_uuids = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

#     # relations output: extraits ordonnés
#     extraits = serializers.SerializerMethodField(read_only=True)

#     def create(self, validated_data):
#         artiste_uuids = validated_data.pop('artiste_uuids', [])
#         interview = Interview.nodes.create(**{k: v for k, v in validated_data.items() if v is not None})

#         # connecter artistes si fournis
#         for a_uuid in artiste_uuids:
#             try:
#                 a = Artiste.nodes.get(uuid=a_uuid)
#                 a.interviews.connect(interview)
#             except DoesNotExist:
#                 raise serializers.ValidationError({'artiste_uuids': f'Artiste introuvable: {a_uuid}'})

#         return interview

#     def update(self, instance, validated_data):
#         artiste_uuids = validated_data.pop('artiste_uuids', None)
#         for k, v in validated_data.items():
#             setattr(instance, k, v)
#         instance.save()

#         if artiste_uuids is not None:
#             # remplacer les relations artistes -> interview par les nouvelles
#             # on va déconnecter tous les artistes qui pointent vers cette interview puis reconnecter
#             q = "MATCH (a:Artiste)-[r:A_PARTICIPE_A]->(i:Interview {uuid:$iid}) DELETE r"
#             db.cypher_query(q, {'iid': instance.uuid})
#             for a_uuid in artiste_uuids:
#                 try:
#                     a = Artiste.nodes.get(uuid=a_uuid)
#                     a.interviews.connect(instance)
#                 except DoesNotExist:
#                     raise serializers.ValidationError({'artiste_uuids': f'Artiste introuvable: {a_uuid}'})
#         return instance


# class ArtisteSerializer(serializers.Serializer):
#     uuid = serializers.CharField(read_only=True)
#     nom = serializers.CharField(required=True)
#     info = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     metadonnees = serializers.JSONField(required=False, allow_null=True)

#     # output: interviews summary
#     interviews = serializers.SerializerMethodField(read_only=True)

#     def get_interviews(self, obj):
#         try:
#             interviews = obj.interviews.all()
#             return [{'uuid': it.uuid, 'titre': it.titre, 'date': it.date} for it in interviews]
#         except Exception:
#             return []

#     def create(self, validated_data):
#         artiste = Artiste.nodes.create(**{k: v for k, v in validated_data.items() if v is not None})
#         return artiste

#     def update(self, instance, validated_data):
#         for k, v in validated_data.items():
#             setattr(instance, k, v)
#         instance.save()
#         return instance


# class UtilisateurSerializer(serializers.Serializer):
#     uuid = serializers.CharField(read_only=True)
#     pseudo = serializers.CharField(required=True)
#     prenom = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     nom = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(write_only=True, required=True)

#     # optional relationships creation via serializer (lists of dicts with uuid + date_heure)
#     recherches_artistes = serializers.ListField(
#         child=serializers.DictField(), write_only=True, required=False,
#         help_text="Liste d'objets {'uuid': artiste_uuid, 'date_heure': ISO_datetime}"
#     )
#     watched_interviews = serializers.ListField(
#         child=serializers.DictField(), write_only=True, required=False
#     )
#     watched_extraits = serializers.ListField(
#         child=serializers.DictField(), write_only=True, required=False
#     )
#     searched_questions = serializers.ListField(
#         child=serializers.DictField(), write_only=True, required=False
#     )

#     def create(self, validated_data):
#         # handle relations lists separately
#         recherches = validated_data.pop('recherches_artistes', [])
#         watched_i = validated_data.pop('watched_interviews', [])
#         watched_e = validated_data.pop('watched_extraits', [])
#         searched_q = validated_data.pop('searched_questions', [])

#         # hash password
#         raw_pwd = validated_data.pop('password')
#         validated_data['password'] = make_password(raw_pwd)

#         user = Utilisateur.nodes.create(**validated_data)

#         # helper to connect relations with date_heure
#         def connect_rel_list(rel_name, target_cls, items):
#             for item in items:
#                 uuid = item.get('uuid')
#                 date_heure = item.get('date_heure')
#                 if not uuid or not date_heure:
#                     raise serializers.ValidationError({rel_name: 'Chaque élément nécessite uuid et date_heure.'})
#                 try:
#                     target = target_cls.nodes.get(uuid=uuid)
#                 except DoesNotExist:
#                     raise serializers.ValidationError({rel_name: f'Target introuvable: {uuid}'})
#                 rel = getattr(user, rel_name)
#                 # connect avec la propriété date_heure
#                 rel.connect(target, {'date_heure': date_heure})

#         connect_rel_list('recherches_artistes', Artiste, recherches)
#         connect_rel_list('watched_interviews', Interview, watched_i)
#         connect_rel_list('watched_extraits', Extrait, watched_e)
#         connect_rel_list('searched_questions', Question, searched_q)

#         return user

#     def update(self, instance, validated_data):
#         # mise à jour simple des champs et du mot de passe si fourni
#         pwd = validated_data.pop('password', None)
#         if pwd:
#             instance.password = make_password(pwd)

#         # update direct properties
#         for k, v in validated_data.items():
#             # ignore relations handled separately in this method
#             if k in ('recherches_artistes', 'watched_interviews', 'watched_extraits', 'searched_questions'):
#                 continue
#             setattr(instance, k, v)
#         instance.save()
#         return instance