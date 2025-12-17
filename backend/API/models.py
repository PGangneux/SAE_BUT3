from neomodel import (
    StructuredNode,
    StringProperty,
    DateProperty,
    UniqueIdProperty,
    IntegerProperty,
    RelationshipTo,
    StructuredRel,
    DateTimeProperty,
    ZeroOrMore,
    BooleanProperty,
    ZeroOrOne,
    RegexProperty,
    EmailProperty,
)
from datetime import date


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

    style = RelationshipTo("StyleMusical", "STYLE", ZeroOrMore)
    nationalite = RelationshipTo("Nation", "NATIONALITE", ZeroOrOne)


class Interview(StructuredNode):
    """
    Noeud Interview
    """

    uuid = UniqueIdProperty()
    titre = RegexProperty(unique_index=True, expression=r".+")
    date = DateProperty(index=True)
    occasion = StringProperty()
    description = StringProperty()
    lieu = StringProperty()

    tags_interview = RelationshipTo("Tag", "TAGS_INTERVIEW", ZeroOrMore)


class Extrait(StructuredNode):
    """
    Noeud Extrait
    """

    uuid = UniqueIdProperty()
    titre = RegexProperty(unique_index=True, expression=r".+")
    description = StringProperty()
    youtube_url = StringProperty()
    vimeo_url = StringProperty()
    uploaded_at = DateProperty(default=date.today())
    duree = IntegerProperty(required=True)  # Nombre de seconde

    interviewer = RelationshipTo("Artiste", "PARTICIPER", ZeroOrOne)
    interviews = RelationshipTo(
        "Interview", "APPARTIENT_A", ZeroOrMore, PositionExtraitRel
    )
    question = RelationshipTo("Question", "POSE", ZeroOrOne)
    tags_extrait = RelationshipTo("Tag", "TAGS_EXTRAIT", ZeroOrMore)


class Question(StructuredNode):
    """
    Noeud Question
    """

    uuid = UniqueIdProperty()
    texte = StringProperty(unique_index=True, required=True)

    theme = RelationshipTo("Theme", "A_THEME", ZeroOrOne)


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
    pseudo = RegexProperty(unique_index=True, required=True, expression=r".+")
    prenom = RegexProperty(required=True, expression=r".+")
    nom = RegexProperty(required=True, expression=r".+")
    email = StringProperty(required=True, unique_index=True)
    # email = EmailProperty(required=True, unique_index=True)
    password = StringProperty(required=True)
    is_admin = BooleanProperty(default=False)

    recherches_artistes = RelationshipTo(
        "Artiste", "RECHERCHES_ARTISTES", ZeroOrMore, DateHeureRel
    )
    regarder_interviews = RelationshipTo(
        "Interview", "REGARDER_INTERVIEWS", ZeroOrMore, DateHeureRel
    )
    regarder_extraits = RelationshipTo(
        "Extrait", "REGARDER_EXTRAITS", ZeroOrMore, DateHeureRel
    )
    recherches_questions = RelationshipTo(
        "Question", "RECHERCHES_QUESTIONS", ZeroOrMore, DateHeureRel
    )


class Nation(StructuredNode):
    """
    Noeud Nation
    """

    uuid = UniqueIdProperty()
    name = RegexProperty(unique_index=True, expression=r".+")


class Tag(StructuredNode):
    """
    Noeud Tag
    """

    uuid = UniqueIdProperty()
    name = RegexProperty(unique_index=True, expression=r".+")
