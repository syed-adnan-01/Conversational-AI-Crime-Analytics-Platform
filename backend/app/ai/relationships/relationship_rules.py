from .relationship_models import RelationshipType

CASE_RELATIONSHIPS = {
    "Victim": RelationshipType.INVOLVED_IN, "Accused": RelationshipType.INVOLVED_IN,
    "Witness": RelationshipType.TESTIFIED_IN, "Evidence": RelationshipType.REFERENCES,
    "Timeline": RelationshipType.REFERENCES, "Officer": RelationshipType.WORKED_ON,
    "Chargesheet": RelationshipType.SUBMITTED,
}
