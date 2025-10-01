from neomodel import (
    db,
    config,
    StructuredNode,
    StringProperty,
    IntegerProperty,
    UniqueIdProperty,
    RelationshipTo
)

class Interview(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)

class Extrait(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    url_youtube = StringProperty()
    appartient = RelationshipTo('Interview', 'APPARTIENT')

class Artiste(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    participer = RelationshipTo('Interview', 'PARTICIPER')

class Theme(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)

class Question(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    correspond = RelationshipTo('Extrait', 'CORRESPOND')
    theme = RelationshipTo('Theme', 'A_POUR_THEME')

class Utilisateur(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    rechercher_artiste = RelationshipTo('Artiste', 'RECHERCHER_ARTISTE')
    rechercher_question = RelationshipTo('Question', 'RECHERCHER_QUESTION')
    visionner_interview = RelationshipTo('Interview', 'VISIONNER_INTERVIEW')
    visionner_extrait = RelationshipTo('Extrait', 'VISIONNER_EXTRAIT')
