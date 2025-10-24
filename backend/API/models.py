from neomodel import (
    StructuredNode, StringProperty, DateProperty, UniqueIdProperty,
    IntegerProperty, RelationshipTo, StructuredRel,
    DateTimeProperty, ZeroOrMore, BooleanProperty,
    ZeroOrOne,
)


class PositionExtraitRel(StructuredRel):
    """
    Relation Postion Extrait
    """
    position = IntegerProperty(required=True)


class DateHeureRel(StructuredRel):
    """
    Relation Date Heure
    """
    date_heure = DateTimeProperty(default_now=True)


class StyleMusical(StructuredNode):
    """
    Noeud Style Musical
    """
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)


class Artiste(StructuredNode):
    """
    Noeud Artiste
    """
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    info = StringProperty()

    style = RelationshipTo('StyleMusical', 'STYLE', ZeroOrMore)
    nationalite = RelationshipTo('Nation', 'NATIONALITE', ZeroOrOne)


class Interview(StructuredNode):
    """
    Noeud Interview
    """
    uuid = UniqueIdProperty()
    titre = StringProperty(index=True, db_property='name')
    date = DateProperty(index=True)
    occasion = StringProperty()
    description = StringProperty()
    lieu = StringProperty()

    tags_interview = RelationshipTo('Tag', 'TAGS_INTERVIEW', ZeroOrMore)


class Extrait(StructuredNode):
    """
    Noeud Extrait
    """
    uuid = UniqueIdProperty()
    titre = StringProperty(db_property='name')
    description = StringProperty()
    youtube_url = StringProperty(unique_index=True)
    vimeo_url = StringProperty(unique_index=True)
    uploaded_at = DateProperty(default_now=True)

    interviewer = RelationshipTo('Artiste', 'PARTICIPER', ZeroOrOne)
    interviews = RelationshipTo('Interview', 'APPARTIENT_A', ZeroOrMore, PositionExtraitRel)
    question = RelationshipTo('Question', 'POSE', ZeroOrOne)
    tags_extrait = RelationshipTo('Tag', 'TAGS_EXTRAIT', ZeroOrMore)


class Question(StructuredNode):
    """
    Noeud Question
    """
    uuid = UniqueIdProperty()
    texte = StringProperty(unique_index=True, required=True, db_property='name')

    theme = RelationshipTo('Theme', 'A_THEME', ZeroOrOne)


class Theme(StructuredNode):
    """
    Noeud Theme
    """
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    description = StringProperty()


class Utilisateur(StructuredNode):
    """
    Noeud Utilisateur
    """
    uuid = UniqueIdProperty()
    pseudo = StringProperty(unique_index=True, required=True, db_property='name')
    prenom = StringProperty(required=True)
    nom = StringProperty(required=True)
    email = StringProperty(required=True, unique_index=True)
    password = StringProperty(required=True)
    is_admin = BooleanProperty(default=False)

    recherches_artistes = RelationshipTo('Artiste', 'RECHERCHES_ARTISTES', ZeroOrMore, DateHeureRel)
    regarder_interviews = RelationshipTo('Interview', 'REGARDER_INTERVIEWS', ZeroOrMore, DateHeureRel)
    regarder_extraits = RelationshipTo('Extrait', 'REGARDER_EXTRAITS', ZeroOrMore, DateHeureRel)
    recherches_questions = RelationshipTo('Question', 'RECHERCHES_QUESTIONS', ZeroOrMore, DateHeureRel)


class Nation(StructuredNode):
    """
    Noeud Nation
    """
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)

class Tag(StructuredNode):
    """
    Noeud Tag
    """
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)