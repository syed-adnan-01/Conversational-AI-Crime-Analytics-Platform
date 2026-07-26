from .entity_models import EntityAlias, EntityRecord, EntityType
from .entity_registry import EntityRegistry

__all__ = ["EntityAlias", "EntityRecord", "EntityType", "EntityRegistry", "EntityResolver"]


def __getattr__(name: str):
    """Avoid importing resolution models while graph models are being initialized."""
    if name == "EntityResolver":
        from .entity_resolver import EntityResolver
        return EntityResolver
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
