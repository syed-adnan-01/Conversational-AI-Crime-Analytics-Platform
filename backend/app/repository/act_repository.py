from copy import deepcopy
from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.act import Act
from app.schemas.act import ActSortField
from app.common.enums import SortOrder
from app.common.queries.act_query import ActQueryOptions
from app.repository.seed.legal_seed import SEED_ACTS


class ActRepository:
    """
    Repository responsible for legislative Act master data access.
    """

    _acts: list[Act] = []

    # ----------------------------------------------------------
    # Initialization & Seeding
    # ----------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the repository. Loads default SEED_ACTS if empty.
        """
        if cls._acts:
            return

        now = datetime.now()
        for seed in SEED_ACTS:
            act = Act(
                act_id=seed["act_id"],
                name=seed["name"],
                short_name=seed["short_name"],
                year=seed["year"],
                description=seed["description"],
                created_at=now,
                updated_at=now,
            )
            cls._acts.append(act)

        app_logger.info("Act repository initialized with %d seeded Acts.", len(cls._acts))

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    @classmethod
    def create_act(cls, act: Act) -> Act:
        """
        Store a new Act master record.
        """
        now = datetime.now()
        stored = act.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )
        cls._acts.append(stored)
        app_logger.info("Act master created | ID=%s | ShortName=%s", stored.act_id, stored.short_name)
        return stored

    # ----------------------------------------------------------
    # Retrieve — By ID
    # ----------------------------------------------------------

    @classmethod
    def get_act_by_id(cls, act_id: str) -> Optional[Act]:
        """
        Retrieve an Act by its ID.
        """
        return next((a for a in cls._acts if a.act_id == act_id), None)

    # ----------------------------------------------------------
    # Retrieve — By Short Name and Year (Unique constraint check)
    # ----------------------------------------------------------

    @classmethod
    def get_act_by_short_name(cls, short_name: str, year: int) -> Optional[Act]:
        """
        Retrieve an Act by its short name and enactment year.
        """
        return next(
            (a for a in cls._acts if a.short_name.lower() == short_name.lower() and a.year == year),
            None,
        )

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    @classmethod
    def update_act(cls, act: Act) -> Optional[Act]:
        """
        Replace an existing Act master record.
        """
        act_id = act.act_id
        for index, existing in enumerate(cls._acts):
            if existing.act_id == act_id:
                updated_record = act.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._acts[index] = updated_record
                app_logger.info("Act master updated | ID=%s", act_id)
                return updated_record
        return None

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    @classmethod
    def delete_act(cls, act_id: str) -> bool:
        """
        Delete an Act from the master catalog.
        """
        for index, existing in enumerate(cls._acts):
            if existing.act_id == act_id:
                del cls._acts[index]
                app_logger.info("Act master deleted | ID=%s", act_id)
                return True
        return False

    # ----------------------------------------------------------
    # Query & Search
    # ----------------------------------------------------------

    @classmethod
    def query_acts(cls, options: ActQueryOptions) -> tuple[list[Act], int]:
        """
        Query Acts with sorting, keyword matching, and pagination.
        """
        filtered = list(cls._acts)

        # 1. Filtering & Search
        if options.name:
            search_name = options.name.lower()
            filtered = [a for a in filtered if search_name in a.name.lower()]

        if options.short_name:
            search_short = options.short_name.lower()
            filtered = [a for a in filtered if search_short in a.short_name.lower()]

        if options.year is not None:
            filtered = [a for a in filtered if a.year == options.year]

        total_count = len(filtered)

        # 2. Sorting Whitelist Mapping
        SORT_FIELDS = {
            ActSortField.NAME: lambda a: a.name.lower(),
            ActSortField.SHORT_NAME: lambda a: a.short_name.lower(),
            ActSortField.YEAR: lambda a: a.year or 0,
            ActSortField.CREATED_DATE: lambda a: a.created_at or datetime.min,
            ActSortField.UPDATED_DATE: lambda a: a.updated_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda a: a.created_at)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        # 3. Pagination
        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
