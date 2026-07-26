from __future__ import annotations

from hashlib import sha256
from typing import Any
from .aliases import aliases_for
from .entity_models import EntityRecord, EntityType


class EntityRegistry:
    """Assigns stable KG identifiers without persisting or altering source records."""
    def __init__(self) -> None:
        self._entities: dict[str, EntityRecord] = {}

    def register(self, entity_type: EntityType, source_id: object, label: str, metadata: dict[str, Any] | None = None) -> EntityRecord:
        raw = f"{entity_type.value}:{source_id}"
        entity_id = "KG-ENTITY-" + sha256(raw.encode()).hexdigest()[:16].upper()
        record = EntityRecord(id=entity_id, entity_type=entity_type, label=label or str(source_id), source_id=str(source_id), metadata=metadata or {}, aliases=aliases_for(label, source_id))
        existing = self._entities.get(entity_id)
        if existing:
            existing.metadata.update(record.metadata)
            return existing
        self._entities[entity_id] = record
        return record

    def get(self, entity_id: str) -> EntityRecord | None:
        return self._entities.get(entity_id)

    def values(self) -> list[EntityRecord]:
        return list(self._entities.values())
