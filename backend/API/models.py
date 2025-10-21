from neomodel import (
    StructuredNode, StringProperty, DateProperty, UniqueIdProperty,
    IntegerProperty, RelationshipTo, StructuredRel,
    DateTimeProperty
)

class PositionExtraitRel(StructuredRel):
    position = IntegerProperty(required=True)

class DateHeureRel(StructuredRel):
    date_heure = DateTimeProperty(required=True)

class StyleMusical(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)


class Artiste(StructuredNode):
    """Noeud Artiste"""
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    info = StringProperty()

    style = RelationshipTo('StyleMusical', 'STYLE')
    nationalite = RelationshipTo('Nation', 'NATIONALITE')


class Interview(StructuredNode):
    """Noeud Interview"""
    uuid = UniqueIdProperty()
    titre = StringProperty(index=True, db_property='name')
    date = DateProperty(index=True)
    occasion = StringProperty()
    description = StringProperty()
    lieu = StringProperty()

    interviewer = RelationshipTo('Artiste', 'PARTICIPER')


class Extrait(StructuredNode):
    """Noeud Extrait (provenant d'une Interview)."""
    uuid = UniqueIdProperty()
    titre = StringProperty(db_property='name')
    description = StringProperty()

    youtube_url = StringProperty(unique_index=True)
    vimeo_url = StringProperty(unique_index=True)
    uploaded_at = DateProperty(default_now=True)

    interview = RelationshipTo('Interview', 'APPARTIENT_A', model=PositionExtraitRel)
    question = RelationshipTo('Question', 'POSE')


class Question(StructuredNode):
    uuid = UniqueIdProperty()
    texte = StringProperty(unique_index=True, required=True, db_property='name')

    theme = RelationshipTo('Theme', 'A_THEME')


class Theme(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    description = StringProperty()


class Utilisateur(StructuredNode):
    uuid = UniqueIdProperty()
    pseudo = StringProperty(unique_index=True, required=True, db_property='name')
    prenom = StringProperty(required=True)
    nom = StringProperty(required=True)
    email = StringProperty(required=True, unique_index=True)
    password = StringProperty(required=True)

    recherches_artistes = RelationshipTo('Artiste', 'RECHERCHE', model=DateHeureRel)
    watched_interviews = RelationshipTo('Interview', 'A_VU', model=DateHeureRel)
    watched_extraits = RelationshipTo('Extrait', 'A_VU', model=DateHeureRel)
    searched_questions = RelationshipTo('Question', 'A_RECHERCHE', model=DateHeureRel)


class Nation(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
