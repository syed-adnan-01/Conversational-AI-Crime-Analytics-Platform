from .entity_models import EntityAlias

def normalise_alias(value: str) -> str:
    return " ".join(value.casefold().split())

def aliases_for(label: str, *values: object) -> list[EntityAlias]:
    unique = {normalise_alias(str(item)): str(item) for item in (label, *values) if item}
    return [EntityAlias(value=value) for value in unique.values()]
