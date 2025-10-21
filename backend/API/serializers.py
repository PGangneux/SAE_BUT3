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
        return {"url": self.context.get('request').build_absolute_uri(reverse('question-list', kwargs={'theme_uuid': theme.uuid}))}

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

    # Inputs
    theme_uuid = serializers.CharField(write_only=True, required=False)

    # Outputs
    theme = serializers.SerializerMethodField(read_only=True)

    def get_theme(self, question):
        """
        Renvoie un lien propre vers le thème
        """
        if question.theme:
            return {"url": self.context.get('request').build_absolute_uri(reverse('theme-detail', kwargs={'uuid': question.theme.single().uuid}))}
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
                raise serializers.ValidationError({"theme_uuid": "Thème introuvable."}, 404)
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
            instance.theme.disconnect(instance.theme.single())
            if theme_uuid:
                instance.theme.connect(Theme.nodes.get(uuid=theme_uuid))
        except Theme.DoesNotExist:
            raise serializers.ValidationError({"theme_uuid": "Thème introuvable."}, 404)
        return instance


class ExtraitSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    youtube_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    vimeo_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    uploaded_at = serializers.DateTimeField(required=False, allow_null=True)

    # Input:
    position = serializers.IntegerField(write_only=True, required=False)    
    interview_uuid = serializers.CharField(write_only=True, required=False)
    question_uuid = serializers.CharField(write_only=True, required=False)

    # Output:
    interview = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)

    def get_interview(self, extrait):
        interview = extrait.interview.single()
        if interview:
            query = "MATCH (i:Interview {uuid:$iid})<-[r:APPARTIENT_A]-(e:Extrait {uuid:$eid}) RETURN i, r"
            res = db.cypher_query(query, {'iid': interview.uuid, 'eid': extrait.uuid})[0]
            if res:
                node = res[0]
                relationship = res[1]
                return {
                    'url': self.context.get('request').build_absolute_uri(reverse('interview-detail', kwargs={'uuid': node.get('uuid')})),
                    'position': relationship.get('position')
                }
        return None

    def get_question(self, extrait):
        qn = extrait.question.single()
        if qn:
            return {"url": self.context.get('request').build_absolute_uri(reverse('interview-detail', kwargs={'uuid': qn.uuid}))}
        return None

    def validate(self, data):
        """
        Si interview_uuid fourni, position doit aussi l'être
        """
        if 'interview_uuid' in data and 'position' not in data:
            raise serializers.ValidationError({
                'position': 'Le champ position est requis quand interview_uuid est fourni.'
            }, 400)
        return data

    def create(self, validated_data):
        interview_uuid = validated_data.pop('interview_uuid', None)
        position = validated_data.pop('position', None)
        question_uuid = validated_data.pop('question_uuid', None)

        extrait = Extrait(**validated_data).save()

        if interview_uuid is not None:
            try:
                interview_node = Interview.nodes.get(uuid=interview_uuid)
            except DoesNotExist:
                raise serializers.ValidationError({'interview_uuid': 'Interview introuvable.'}, 404)
            # connecter avec propriété position
            extrait.interview.connect(interview_node, {'position': position})

        if question_uuid is not None:
            try:
                question_node = Question.nodes.get(uuid=question_uuid)
            except DoesNotExist:
                raise serializers.ValidationError({'question_uuid': 'Question introuvable.'}, 404)
            extrait.question.connect(question_node)

        return extrait

    def update(self, extrait, validated_data):
        interview_uuid = validated_data.pop('interview_uuid', None)
        position = validated_data.pop('position', None)
        question_uuid = validated_data.pop('question_uuid', None)

        # update props
        for k, v in validated_data.items():
            setattr(extrait, k, v)
        extrait.save()

        # update interview relation if provided
        if interview_uuid is not None:
            try:
                interview = Interview.nodes.get(uuid=interview_uuid)
            except DoesNotExist:
                raise serializers.ValidationError({'interview_uuid': 'Interview introuvable.'})
            # Disconnect existing interview relations then connect new with position
            try:
                extrait.interview.disconnect(extrait.interview.single())
            except Exception:
                pass
            extrait.interview.connect(interview, {'position': position})

        # update question relation if provided
        if question_uuid is not None:
            try:
                question = Question.nodes.get(uuid=question_uuid)
            except DoesNotExist:
                raise serializers.ValidationError({'question_uuid': 'Question introuvable.'})
            try:
                extrait.question.disconnect(extrait.question.single())
            except Exception:
                pass
            extrait.question.connect(question)

        return extrait


class InterviewSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date = serializers.DateField(required=False, allow_null=True)
    occasion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lieu = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # relations input: lier un artiste à l'interview
    artiste_uuid = serializers.CharField(write_only=True, required=False)

    # relations output: extraits ordonnés
    artiste = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def get_artiste(self, interview):
        if interview.interviewer:
            return {"url": self.context.get('request').build_absolute_uri(reverse('artiste-detail', kwargs={'uuid': interview.interviewer.single().uuid}))}
        return None

    def get_extraits(self, interview):
        return {"url": self.context.get('request').build_absolute_uri(reverse('extrait-list', kwargs={'interview_uuid': interview.uuid}))}

    def create(self, validated_data):
        artiste_uuid = validated_data.pop("artiste_uuid", None)
        interview = Interview(**validated_data).save()
        if artiste_uuid:
            try:
                artiste = Artiste.nodes.get(uuid=artiste_uuid)
                interview.interviewer.connect(artiste)
            except Artiste.DoesNotExist:
                raise serializers.ValidationError({"artiste_uuid": "Artiste introuvable."}, 404)
        return interview

    def update(self, instance, validated_data):
        artiste_uuid = validated_data.pop("artiste_uuid", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        try:
            if instance.interviewer:
                instance.interviewer.disconnect(instance.interviewer.single())
            if artiste_uuid:
                instance.interviewer.connect(Artiste.nodes.get(uuid=artiste_uuid))
        except Artiste.DoesNotExist:
            raise serializers.ValidationError({"artiste_uuid": "Artiste introuvable."}, 404)
        return instance


class ArtisteSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    info = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Output
    # interviews = serializers.SerializerMethodField(read_only=True)

    # def get_interviews(self, obj):
    #     try:
    #         interviews = obj.interviews.all()
    #         return [{'uuid': it.uuid, 'titre': it.titre, 'date': it.date} for it in interviews]
    #     except Exception:
    #         return []

    def create(self, validated_data):
        return Artiste(**validated_data).save()

    def update(self, artiste, validated_data):
        for k, v in validated_data.items():
            setattr(artiste, k, v)
        return artiste.save()


class UtilisateurSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    pseudo = serializers.CharField(required=True)
    prenom = serializers.CharField(required=True)
    nom = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

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