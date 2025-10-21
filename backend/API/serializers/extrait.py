from django.urls import reverse
from rest_framework import serializers
from neomodel.exceptions import DoesNotExist
from neomodel import db
from ..models import Interview, Extrait, Question


class ExtraitSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    youtube_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    vimeo_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    uploaded_at = serializers.DateField(required=False, allow_null=True)

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
            res = db.cypher_query(query, {'iid': interview.uuid, 'eid': extrait.uuid})[0][0]
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
            return {"url": self.context.get('request').build_absolute_uri(reverse('question-detail', kwargs={'uuid': qn.uuid}))}
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
