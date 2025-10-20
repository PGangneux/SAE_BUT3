from neomodel import (
    StructuredNode, StringProperty, DateProperty, UniqueIdProperty,
    IntegerProperty, RelationshipTo, StructuredRel,
    DateTimeProperty, JSONProperty
)

class PositionExtraitRel(StructuredRel):
    position = IntegerProperty(required=True)

class DateHeureRel(StructuredRel):
    date_heure = DateTimeProperty(required=True)


class Artiste(StructuredNode):
    """Noeud Artiste"""
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    info = StringProperty()
    metadonnees = JSONProperty()

    interviews = RelationshipTo('Interview', 'A_PARTICIPE_A')


class Interview(StructuredNode):
    """Noeud Interview"""
    uuid = UniqueIdProperty()
    titre = StringProperty(index=True, db_property='name')
    date = DateProperty(index=True)
    occasion = StringProperty()
    description = StringProperty()
    lieu = StringProperty()
    metadonnees = JSONProperty()


class Extrait(StructuredNode):
    """Noeud Extrait (provenant d'une Interview)."""
    uuid = UniqueIdProperty()
    titre = StringProperty(db_property='name')
    description = StringProperty()
    metadonnees = JSONProperty()

    youtube_url = StringProperty(unique_index=True)
    vimeo_url = StringProperty(unique_index=True)
    uploaded_at = DateTimeProperty(default_now=True)

    interview = RelationshipTo('Interview', 'APPARTIENT_A', model=PositionExtraitRel)
    question = RelationshipTo('Question', 'POSE')


class Question(StructuredNode):
    uuid = UniqueIdProperty()
    texte = StringProperty(unique_index=True, required=True, db_property='name')
    variantes = JSONProperty()

    theme = RelationshipTo('Theme', 'APPARTIENT_A')


class Theme(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    description = StringProperty()


class Utilisateur(StructuredNode):
    uuid = UniqueIdProperty()
    pseudo = StringProperty(index=True, required=True, db_property='name')
    prenom = StringProperty()
    nom = StringProperty()
    email = StringProperty(required=True, unique_index=True)
    password = StringProperty(required=True)

    recherches_artistes = RelationshipTo('Artiste', 'RECHERCHE', model=DateHeureRel)
    watched_interviews = RelationshipTo('Interview', 'A_VU', model=DateHeureRel)
    watched_extraits = RelationshipTo('Extrait', 'A_VU', model=DateHeureRel)
    searched_questions = RelationshipTo('Question', 'A_RECHERCHE', model=DateHeureRel)
