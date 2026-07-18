from uuid import uuid4
from fastapi import Depends

from app.common.exceptions import ActNotFoundException, DuplicateActException
from app.models.act import Act
from app.repository.act_repository import ActRepository
from app.common.queries.act_query import ActQueryOptions
from app.schemas.act import (
    ActCreate,
    ActResponse,
    ActSummary,
    ActListResponse,
    PaginationMeta,
    ActUpdate,
)


class ActService:
    """
    Service layer handling legislative Act catalog logic.
    """

    def __init__(
        self,
        act_repo: ActRepository = Depends(lambda: ActRepository),
    ):
        self.act_repo = act_repo

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    def create_act(self, schema: ActCreate) -> ActResponse:
        """
        Create a new Act master record.
        Ensures name, short_name, and year constraints.
        """
        short_name = schema.short_name.strip()
        name = schema.name.strip()

        # Check unique constraint (short_name + year)
        existing = self.act_repo.get_act_by_short_name(short_name, schema.year)
        if existing is not None:
            raise DuplicateActException(short_name, schema.year)

        # Generate Act ID in Service
        act_id = f"ACT-{uuid4().hex[:12].upper()}"

        act = Act(
            act_id=act_id,
            name=name,
            short_name=short_name,
            year=schema.year,
            description=schema.description,
        )

        stored = self.act_repo.create_act(act)
        return ActResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Retrieve
    # ----------------------------------------------------------

    def get_act(self, act_id: str) -> ActResponse:
        """
        Retrieve Act details.
        """
        act = self.act_repo.get_act_by_id(act_id)
        if act is None:
            raise ActNotFoundException(act_id)
        return ActResponse.model_validate(act)

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    def update_act(self, act_id: str, schema: ActUpdate) -> ActResponse:
        """
        Update an Act master record.
        """
        existing = self.act_repo.get_act_by_id(act_id)
        if existing is None:
            raise ActNotFoundException(act_id)

        updates = schema.model_dump(exclude_unset=True)

        if "short_name" in updates or "year" in updates:
            updated_short = updates.get("short_name", existing.short_name).strip()
            updated_year = updates.get("year", existing.year)

            if updated_short != existing.short_name or updated_year != existing.year:
                # Check for duplicate
                other = self.act_repo.get_act_by_short_name(updated_short, updated_year)
                if other is not None and other.act_id != act_id:
                    raise DuplicateActException(updated_short, updated_year)
                
                updates["short_name"] = updated_short

        if "name" in updates:
            updates["name"] = updates["name"].strip()

        updated_act = existing.model_copy(update=updates)
        stored = self.act_repo.update_act(updated_act)

        if stored is None:
            raise ActNotFoundException(act_id)

        return ActResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    def delete_act(self, act_id: str) -> None:
        """
        Delete an Act from the catalog.
        """
        existing = self.act_repo.get_act_by_id(act_id)
        if existing is None:
            raise ActNotFoundException(act_id)
        self.act_repo.delete_act(act_id)

    # ----------------------------------------------------------
    # Search
    # ----------------------------------------------------------

    def search_acts(self, options: ActQueryOptions) -> ActListResponse:
        """
        Search legislative acts.
        """
        records, total = self.act_repo.query_acts(options)
        summaries = [ActSummary.model_validate(a) for a in records]
        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )
        return ActListResponse(items=summaries, pagination=meta)
