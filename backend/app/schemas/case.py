"""
============================================================
Case Management Schemas — API Contract Layer
============================================================

Module  : Case Management (Phase 2 — Pydantic Schemas)
Source   : CaseMaster Domain Model (Phase 1)
Author  : CrimeSphere AI Architecture Team

------------------------------------------------------------
PURPOSE
------------------------------------------------------------
These schemas define the API contract between the frontend
and backend for the Case Management module. They are
intentionally SEPARATE from the CaseMaster domain model:

  • Domain Model  → internal business entity (models/)
  • Schemas        → external API surface     (schemas/)

This separation ensures that database changes never break
the frontend API, and vice versa.

------------------------------------------------------------
INHERITANCE STRATEGY
------------------------------------------------------------

CaseBase
  ├── CaseCreate      (client → server: registration)
  ├── CaseUpdate      (client → server: mutation)
  └── CaseResponse    (server → client: full detail)

CaseSummary           (standalone — dashboard/list view)
CaseListResponse      (paginated wrapper around CaseSummary)
CaseSearchFilters     (standalone — query parameter contract)

CaseBase exists ONLY because CaseCreate, CaseUpdate, and
CaseResponse share ~12 overlapping fields. Without it, each
schema would duplicate those fields identically. The base
is kept minimal — it holds only the shared classification
and incident fields, not identifiers or audit timestamps.

CaseSummary does NOT inherit from CaseBase because it uses
a fundamentally different field subset (flattened labels
instead of raw IDs). Forcing inheritance would couple the
dashboard view to the detail view unnecessarily.

------------------------------------------------------------
FUTURE EXTENSIBILITY
------------------------------------------------------------

These schemas are designed so the following can be appended
in future phases WITHOUT breaking the existing API contract:

  • victims: list[VictimSummary]
  • accused: list[AccusedSummary]
  • complainant: ComplainantSummary
  • evidence: list[EvidenceSummary]
  • ai_analysis: AIAnalysisResult
  • graph_relationships: list[GraphEdge]
  • timeline: list[TimelineEvent]
  • attachments: list[Attachment]
  • officer_details: OfficerDetail
  • court_details: CourtDetail

Adding any of these to CaseResponse requires only a new
Optional field — no schema restructuring.
"""

from datetime import datetime
from enum import Enum
from math import ceil
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ==============================================================
# BASE SCHEMA
# ==============================================================

class CaseBase(BaseModel):
    """
    Shared fields between CaseCreate, CaseUpdate, and CaseResponse.

    Contains classification, incident, geospatial, and narrative
    fields that appear in all three schemas. Identifiers and audit
    timestamps are intentionally excluded — they differ per schema.
    """

    # ----------------------------------------------------------
    # Reference IDs — Police Personnel
    # ----------------------------------------------------------

    # Investigating officer assigned to this case.
    # References PolicePerson module (not yet implemented).
    police_person_id: Optional[int] = Field(
        default=None,
        description="ID of the investigating officer assigned to this case.",
        examples=[1042],
    )

    # ----------------------------------------------------------
    # Reference IDs — Classification & Categorization
    # ----------------------------------------------------------

    # Case category (e.g., Cognizable, Non-Cognizable).
    # References CaseCategory lookup (not yet implemented).
    case_category_id: Optional[int] = Field(
        default=None,
        description="ID of the case category (Cognizable, Non-Cognizable, etc.).",
        examples=[1],
    )

    # Gravity/severity of the offence.
    # References GravityOffence lookup (not yet implemented).
    gravity_offence_id: Optional[int] = Field(
        default=None,
        description="ID indicating the gravity/severity of the offence.",
        examples=[3],
    )

    # Major classification head of the crime.
    # References CrimeMajorHead lookup (not yet implemented).
    crime_major_head_id: Optional[int] = Field(
        default=None,
        description="Major crime classification head (e.g., Crimes Against Person).",
        examples=[5],
    )

    # Sub-classification under the major head.
    # References CrimeMinorHead lookup (not yet implemented).
    crime_minor_head_id: Optional[int] = Field(
        default=None,
        description="Minor crime classification under the major head.",
        examples=[12],
    )

    # ----------------------------------------------------------
    # Reference IDs — Case Lifecycle
    # ----------------------------------------------------------

    # Current lifecycle status of the case.
    # References CaseStatus lookup (not yet implemented).
    case_status_id: Optional[int] = Field(
        default=None,
        description="Current case lifecycle status (Registered, Under Investigation, etc.).",
        examples=[1],
    )

    # Court where the case is being tried.
    # References Court module (not yet implemented).
    # Nullable — assigned after chargesheet is filed.
    court_id: Optional[int] = Field(
        default=None,
        description="ID of the court where the case is being tried.",
        examples=[7],
    )

    # ----------------------------------------------------------
    # Temporal Fields — Incident Window
    # ----------------------------------------------------------

    # Start of the incident window.
    incident_from_date: Optional[datetime] = Field(
        default=None,
        description="Start date/time of the incident.",
        examples=["2026-07-15T14:30:00"],
    )

    # End of the incident window.
    incident_to_date: Optional[datetime] = Field(
        default=None,
        description="End date/time of the incident.",
        examples=["2026-07-15T18:45:00"],
    )

    # When the information was received at the police station.
    # May differ from the registration date in delayed reports.
    info_received_ps_date: Optional[datetime] = Field(
        default=None,
        description="Date/time the information was received at the police station.",
        examples=["2026-07-15T20:00:00"],
    )

    # ----------------------------------------------------------
    # Geospatial Fields
    # ----------------------------------------------------------

    # GPS latitude of the incident location.
    # Structural validation: must be a valid latitude [-90, 90].
    latitude: Optional[float] = Field(
        default=None,
        ge=-90.0,
        le=90.0,
        description="GPS latitude of the incident location.",
        examples=[19.0760],
    )

    # GPS longitude of the incident location.
    # Structural validation: must be a valid longitude [-180, 180].
    longitude: Optional[float] = Field(
        default=None,
        ge=-180.0,
        le=180.0,
        description="GPS longitude of the incident location.",
        examples=[72.8777],
    )

    # ----------------------------------------------------------
    # Narrative / Descriptive Content
    # ----------------------------------------------------------

    # Free-text summary of the incident.
    # Primary input for the AI NLP analysis pipeline.
    # Structural validation: max 10,000 characters.
    brief_facts: Optional[str] = Field(
        default=None,
        max_length=10000,
        description="Free-text summary of the incident as recorded in the FIR.",
        examples=["Complainant reported theft of mobile phone from local market."],
    )


# ==============================================================
# 1. CaseCreate — Registration Request
# ==============================================================

class CaseCreate(CaseBase):
    """
    Schema for registering a new FIR / case.

    Sent by the client when creating a new case record.
    Contains only fields the client is allowed to provide.

    Excluded (system-generated):
      • case_master_id  — assigned by the datastore
      • case_no         — assigned by the court post-chargesheet
      • created_at      — set by the repository layer
      • updated_at      — set by the repository layer
    """

    # ----------------------------------------------------------
    # FIR Registration — Required
    # ----------------------------------------------------------

    # Official crime number assigned by the police station.
    # Structural validation: 1–50 characters.
    crime_no: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Official Crime Number assigned by the police station.",
        examples=["0045/2026"],
    )

    # Date and time the FIR was officially registered.
    crime_registered_date: datetime = Field(
        ...,
        description="Date and time the FIR was officially registered.",
        examples=["2026-07-18T10:30:00"],
    )

    # Police station where the FIR was registered.
    # References PoliceStation module (not yet implemented).
    police_station_id: int = Field(
        ...,
        gt=0,
        description="ID of the police station where the FIR was registered.",
        examples=[101],
    )


# ==============================================================
# 2. CaseUpdate — Mutation Request
# ==============================================================

class CaseUpdate(CaseBase):
    """
    Schema for updating an existing case record.

    Every field is optional — only provided fields are updated.
    Immutable fields are excluded to prevent accidental mutation.

    Immutable (cannot be changed after creation):
      • case_master_id       — primary key
      • crime_no             — legal identifier, immutable once registered
      • case_no              — court-assigned, immutable once set
      • crime_registered_date — official registration timestamp
      • police_station_id    — station of original registration
      • created_at           — audit trail integrity
    """

    # No additional required fields.
    # All mutable fields are inherited from CaseBase as Optional.
    # The service layer will apply only non-None values.
    pass


# ==============================================================
# 3. CaseResponse — Full Detail View
# ==============================================================

class CaseResponse(CaseBase):
    """
    Complete case record returned to the frontend.

    Includes all fields: identifiers, registration data,
    classification, incident window, geospatial coordinates,
    narrative content, and audit timestamps.

    Future phases will append nested objects here:
      • victims, accused, complainant
      • evidence, AI analysis
      • officer_details, court_details
      • graph_relationships, timeline, attachments
    """

    model_config = ConfigDict(from_attributes=True)

    # ----------------------------------------------------------
    # Primary Identifier
    # ----------------------------------------------------------

    # System-generated unique identifier.
    case_master_id: str = Field(
        ...,
        description="Unique system-generated identifier for the case record.",
        examples=["cm_a1b2c3d4e5f6"],
    )

    # ----------------------------------------------------------
    # FIR Registration Identifiers
    # ----------------------------------------------------------

    # Official crime number — immutable after registration.
    crime_no: str = Field(
        ...,
        description="Official Crime Number assigned by the police station.",
        examples=["0045/2026"],
    )

    # Court-assigned case number — null until chargesheet is filed.
    case_no: Optional[str] = Field(
        default=None,
        description="Court-assigned Case Number (set after chargesheet filing).",
        examples=["SC-2026-0012"],
    )

    # ----------------------------------------------------------
    # Registration Metadata
    # ----------------------------------------------------------

    # Date and time the FIR was officially registered.
    crime_registered_date: datetime = Field(
        ...,
        description="Date and time the FIR was officially registered.",
        examples=["2026-07-18T10:30:00"],
    )

    # Police station where the FIR was registered.
    police_station_id: int = Field(
        ...,
        description="ID of the police station where the FIR was registered.",
        examples=[101],
    )

    # ----------------------------------------------------------
    # Audit Timestamps
    # ----------------------------------------------------------

    # Record creation timestamp — set by the repository.
    created_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when this case record was created.",
        examples=["2026-07-18T10:30:00"],
    )

    # Last modification timestamp — updated on each mutation.
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of the most recent update to this record.",
        examples=["2026-07-18T15:45:00"],
    )


# ==============================================================
# 4. CaseSummary — Dashboard / List View
# ==============================================================

class CaseSummary(BaseModel):
    """
    Lightweight case representation for dashboards, search
    results, and table listings.

    Does NOT inherit from CaseBase — intentionally different
    field set. Uses only the minimum fields needed to identify
    and contextualize a case in a list view. Raw foreign-key
    IDs are retained for now; future phases may replace them
    with resolved display labels (e.g., station name, officer
    name) via response enrichment in the service layer.
    """

    model_config = ConfigDict(from_attributes=True)

    # System-generated unique identifier.
    case_master_id: str = Field(
        ...,
        description="Unique system-generated identifier for the case record.",
        examples=["cm_a1b2c3d4e5f6"],
    )

    # Official crime number.
    crime_no: str = Field(
        ...,
        description="Official Crime Number assigned by the police station.",
        examples=["0045/2026"],
    )

    # Court-assigned case number (null until chargesheet).
    case_no: Optional[str] = Field(
        default=None,
        description="Court-assigned Case Number.",
        examples=["SC-2026-0012"],
    )

    # Current lifecycle status.
    # Will display as a badge/chip in the frontend.
    case_status_id: Optional[int] = Field(
        default=None,
        description="Current case lifecycle status ID.",
        examples=[1],
    )

    # Date the FIR was registered — primary sort field.
    crime_registered_date: datetime = Field(
        ...,
        description="Date and time the FIR was officially registered.",
        examples=["2026-07-18T10:30:00"],
    )

    # Police station where the FIR was registered.
    police_station_id: int = Field(
        ...,
        description="ID of the police station where the FIR was registered.",
        examples=[101],
    )

    # Major classification head — gives context in list view.
    crime_major_head_id: Optional[int] = Field(
        default=None,
        description="Major crime classification head ID.",
        examples=[5],
    )

    # Investigating officer — shows assignment status.
    police_person_id: Optional[int] = Field(
        default=None,
        description="ID of the investigating officer assigned to this case.",
        examples=[1042],
    )


# ==============================================================
# 5. CaseListResponse — Paginated Wrapper
# ==============================================================

class PaginationMeta(BaseModel):
    """
    Pagination metadata returned alongside list responses.

    Designed to support offset-based SQL pagination.
    Can be extended for cursor-based pagination in future
    phases (e.g., for infinite scroll or real-time feeds).
    """

    # Total number of records matching the query.
    total: int = Field(
        ...,
        ge=0,
        description="Total number of records matching the query.",
        examples=[142],
    )

    # Current page number (1-indexed).
    page: int = Field(
        ...,
        ge=1,
        description="Current page number (1-indexed).",
        examples=[1],
    )

    # Number of records per page.
    page_size: int = Field(
        ...,
        ge=1,
        le=100,
        description="Number of records returned per page.",
        examples=[20],
    )

    # Total number of pages.
    total_pages: int = Field(
        ...,
        ge=0,
        description="Total number of pages available.",
        examples=[8],
    )

    # Indicates if there is a next page.
    has_next: bool = Field(
        ...,
        description="True if there is a next page of records available.",
        examples=[True],
    )

    # Indicates if there is a previous page.
    has_previous: bool = Field(
        ...,
        description="True if there is a previous page of records available.",
        examples=[False],
    )

    @staticmethod
    def calculate(total: int, page: int, page_size: int) -> "PaginationMeta":
        """
        Factory method to compute pagination metadata.

        Not business logic — purely arithmetic over page parameters.
        """
        total_pages = ceil(total / page_size) if page_size > 0 else 0
        return PaginationMeta(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )


class CaseListResponse(BaseModel):
    """
    Paginated list of case summaries.

    Never returns a raw list — always wraps items with
    pagination metadata for consistent frontend consumption.
    """

    # List of case summaries for the current page.
    items: list[CaseSummary] = Field(
        ...,
        description="List of case summary records for the current page.",
    )

    # Pagination metadata.
    pagination: PaginationMeta = Field(
        ...,
        description="Pagination metadata for the current result set.",
    )


# ==============================================================
# 6. CaseSearchFilters — Query Parameter Contract
# ==============================================================

class SortField(str, Enum):
    REGISTERED_DATE = "registered_date"
    INCIDENT_DATE = "incident_date"
    CASE_NUMBER = "case_number"
    CRIME_NUMBER = "crime_number"
    CREATED_DATE = "created_date"
    UPDATED_DATE = "updated_date"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class CaseFilterParams(BaseModel):
    """
    Filter sub-schema containing optional query parameters.
    """
    # Identifiers
    case_no: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Filter by court-assigned case number (exact match).",
        examples=["SC-2026-0012"],
    )
    case_number: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Semantic alias for case_no.",
    )
    crime_no: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Filter by crime number (exact match).",
        examples=["0045/2026"],
    )
    crime_number: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Semantic alias for crime_no.",
    )

    # Date ranges
    date_from: Optional[datetime] = Field(
        default=None,
        description="Filter cases registered on or after this date.",
    )
    registered_from_date: Optional[datetime] = Field(
        default=None,
        description="Semantic alias for date_from.",
    )
    date_to: Optional[datetime] = Field(
        default=None,
        description="Filter cases registered on or before this date.",
    )
    registered_to_date: Optional[datetime] = Field(
        default=None,
        description="Semantic alias for date_to.",
    )
    incident_from_date: Optional[datetime] = Field(
        default=None,
        description="Filter cases incident occurred on or after this date.",
    )
    incident_to_date: Optional[datetime] = Field(
        default=None,
        description="Filter cases incident occurred on or before this date.",
    )

    # Classifications
    case_status_id: Optional[int] = Field(
        default=None,
        description="Filter by case lifecycle status ID.",
    )
    case_status: Optional[int] = Field(
        default=None,
        description="Semantic alias for case_status_id.",
    )
    case_category_id: Optional[int] = Field(
        default=None,
        description="Filter by case category ID.",
    )
    crime_category: Optional[int] = Field(
        default=None,
        description="Semantic alias for case_category_id.",
    )
    gravity_offence_id: Optional[int] = Field(
        default=None,
        description="Filter by gravity offence ID.",
    )
    gravity_offence: Optional[int] = Field(
        default=None,
        description="Semantic alias for gravity_offence_id.",
    )
    crime_major_head_id: Optional[int] = Field(
        default=None,
        description="Filter by major crime classification head ID.",
    )
    crime_major_head: Optional[int] = Field(
        default=None,
        description="Semantic alias for crime_major_head_id.",
    )
    crime_minor_head_id: Optional[int] = Field(
        default=None,
        description="Filter by minor crime classification head ID.",
    )
    crime_minor_head: Optional[int] = Field(
        default=None,
        description="Semantic alias for crime_minor_head_id.",
    )

    # Organization
    police_station_id: Optional[int] = Field(
        default=None,
        description="Filter by police station ID.",
    )
    police_station: Optional[int] = Field(
        default=None,
        description="Semantic alias for police_station_id.",
    )
    police_person_id: Optional[int] = Field(
        default=None,
        description="Filter by investigating officer ID.",
    )
    police_person: Optional[int] = Field(
        default=None,
        description="Semantic alias for police_person_id.",
    )
    court_id: Optional[int] = Field(
        default=None,
        description="Filter by court ID.",
    )
    court: Optional[int] = Field(
        default=None,
        description="Semantic alias for court_id.",
    )
    district: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Filter by district name.",
    )
    state: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Filter by state name.",
    )

    # Keyword Search
    brief_facts: Optional[str] = Field(
        default=None,
        description="Case-insensitive keyword search on brief_facts.",
    )


class CaseSortParams(BaseModel):
    """
    Sorting sub-schema.
    """
    sort_by: SortField = Field(
        default=SortField.REGISTERED_DATE,
        description="Field to sort by.",
    )
    sort_order: SortOrder = Field(
        default=SortOrder.DESC,
        description="Sort order (asc or desc).",
    )


class CasePaginationParams(BaseModel):
    """
    Pagination sub-schema.
    """
    page: int = Field(
        default=1,
        ge=1,
        description="Page number (1-indexed).",
    )
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of records per page.",
    )


class CaseSearchFilters(BaseModel):
    """
    Composed schema representing the full case search contract.
    """
    filters: CaseFilterParams = Field(
        default_factory=CaseFilterParams,
        description="Filtering parameters.",
    )
    sort: CaseSortParams = Field(
        default_factory=CaseSortParams,
        description="Sorting parameters.",
    )
    pagination: CasePaginationParams = Field(
        default_factory=CasePaginationParams,
        description="Pagination parameters.",
    )
