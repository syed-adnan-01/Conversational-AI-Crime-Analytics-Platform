from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.officer import OfficerMaster, OfficerAssignment
from app.schemas.officer import OfficerSortField
from app.common.enums import SortOrder
from app.common.queries.officer_query import OfficerAssignmentQueryOptions


class OfficerRepository:
    """
    Repository responsible for Officer Master profiles and transactional Officer Assignments.
    """

    _officers: list[OfficerMaster] = []
    _assignments: list[OfficerAssignment] = []

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory officer store.
        """
        if cls._officers or cls._assignments:
            return
        app_logger.info("Officer repository initialized.")

    # ----------------------------------------------------------
    # Officer Master Operations
    # ----------------------------------------------------------

    @classmethod
    def create_officer(cls, officer: OfficerMaster) -> OfficerMaster:
        """
        Store an OfficerMaster profile.
        """
        now = datetime.now()
        stored = officer.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )
        cls._officers.append(stored)
        app_logger.info("Officer stored | ID=%s | Badge=%s", stored.officer_id, stored.badge_number)
        return stored

    @classmethod
    def get_officer_by_id(cls, officer_id: str) -> Optional[OfficerMaster]:
        """
        Get officer profile by ID.
        """
        return next((o for o in cls._officers if o.officer_id == officer_id), None)

    @classmethod
    def get_officer_by_badge(cls, badge_number: str) -> Optional[OfficerMaster]:
        """
        Get officer profile by badge number.
        """
        return next((o for o in cls._officers if o.badge_number.lower() == badge_number.lower()), None)

    @classmethod
    def list_officers(cls) -> list[OfficerMaster]:
        """
        List all officer master profiles.
        """
        return list(cls._officers)

    # ----------------------------------------------------------
    # Officer Assignment Operations
    # ----------------------------------------------------------

    @classmethod
    def create_assignment(cls, assignment: OfficerAssignment) -> OfficerAssignment:
        """
        Store an OfficerAssignment record.
        """
        now = datetime.now()
        stored = assignment.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )
        cls._assignments.append(stored)
        app_logger.info("Officer assignment stored | ID=%s | CaseID=%s", stored.assignment_id, stored.case_master_id)
        return stored

    @classmethod
    def get_assignment_by_id(cls, assignment_id: str) -> Optional[OfficerAssignment]:
        """
        Retrieve assignment by ID.
        """
        return next((a for a in cls._assignments if a.assignment_id == assignment_id), None)

    @classmethod
    def update_assignment(cls, assignment: OfficerAssignment) -> Optional[OfficerAssignment]:
        """
        Update an assignment record.
        """
        assignment_id = assignment.assignment_id
        for index, existing in enumerate(cls._assignments):
            if existing.assignment_id == assignment_id:
                updated_record = assignment.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._assignments[index] = updated_record
                app_logger.info("Officer assignment updated | ID=%s", assignment_id)
                return updated_record
        return None

    @classmethod
    def delete_assignment(cls, assignment_id: str) -> bool:
        """
        Delete an assignment record.
        """
        for index, existing in enumerate(cls._assignments):
            if existing.assignment_id == assignment_id:
                del cls._assignments[index]
                app_logger.info("Officer assignment deleted | ID=%s", assignment_id)
                return True
        return False

    @classmethod
    def query_assignments(
        cls, options: OfficerAssignmentQueryOptions
    ) -> tuple[list[OfficerAssignment], int]:
        """
        Query assignments with options.
        """
        filtered = list(cls._assignments)

        if options.case_master_id:
            filtered = [a for a in filtered if a.case_master_id == options.case_master_id]

        if options.officer_id:
            filtered = [a for a in filtered if a.officer_id == options.officer_id]

        if options.role:
            filtered = [a for a in filtered if a.role == options.role]

        if options.is_active is not None:
            filtered = [a for a in filtered if a.is_active == options.is_active]

        total_count = len(filtered)

        SORT_FIELDS = {
            OfficerSortField.ASSIGNED_DATE: lambda a: a.assigned_date or datetime.min,
            OfficerSortField.ROLE: lambda a: a.role.value,
            OfficerSortField.CREATED_AT: lambda a: a.created_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda a: a.assigned_date or datetime.min)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
