"""
============================================================
CaseMaster Domain Model
============================================================

Module  : Case Management (Phase 1 — Domain Foundation)
Entity  : CaseMaster
Source   : Police FIR System ER Diagram (Primary Source of Truth)
Author  : CrimeSphere AI Architecture Team

------------------------------------------------------------
PURPOSE
------------------------------------------------------------
CaseMaster is the central aggregate root of the Case Management
bounded context. Every FIR (First Information Report) registered
in the system is represented by a single CaseMaster record.

All downstream entities — Victims, Accused, Evidence, Arrests,
Chargesheets, and AI Analysis — link back to this model.

------------------------------------------------------------
FUTURE RELATIONSHIP MAP
------------------------------------------------------------

                        ┌──────────────┐
                        │  CaseMaster  │  ◄── Aggregate Root
                        └──────┬───────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                     │
    ┌─────▼──────┐     ┌──────▼───────┐     ┌──────▼───────┐
    │   Victims  │     │   Accused    │     │ Complainant  │
    └────────────┘     └──────────────┘     └──────────────┘
          │                    │
    ┌─────▼──────┐     ┌──────▼───────┐
    │  Evidence  │     │   Arrests    │
    └────────────┘     └──────────────┘
          │                    │
    ┌─────▼──────┐     ┌──────▼───────┐
    │ Act Sections│    │ Chargesheet  │
    └────────────┘     └──────────────┘
          │
    ┌─────▼──────────────────────────────┐
    │         AI Analysis Layer          │
    │  (Predictions · Patterns · Graphs) │
    └────────────────────────────────────┘
          │
    ┌─────▼──────────────────────────────┐
    │      Neo4j Knowledge Graph         │
    │  (Criminal Network · Geospatial)   │
    └────────────────────────────────────┘

------------------------------------------------------------
DEPENDENCY REFERENCES (Stored as Primitive IDs)
------------------------------------------------------------

The following fields reference entities from modules that
have NOT been implemented yet. They are stored as primitive
integer/string IDs and will be upgraded to typed foreign
key references or embedded objects in future phases:

  • police_person_id     → PolicePerson module      (Future)
  • police_station_id    → PoliceStation module      (Future)
  • case_category_id     → CaseCategory lookup       (Future)
  • gravity_offence_id   → GravityOffence lookup     (Future)
  • crime_major_head_id  → CrimeMajorHead lookup     (Future)
  • crime_minor_head_id  → CrimeMinorHead lookup     (Future)
  • case_status_id       → CaseStatus lookup/enum    (Future)
  • court_id             → Court module              (Future)

------------------------------------------------------------
ENUM CANDIDATES (Documented — Not Yet Implemented)
------------------------------------------------------------

The following fields are candidates for Python Enum classes
in future phases. See the architecture artifact for the
rationale behind each recommendation.

  • case_status_id       → CaseStatus enum           (RECOMMENDED)
  • case_category_id     → CaseCategory enum         (RECOMMENDED)
  • gravity_offence_id   → GravityOffence enum       (CONDITIONAL)
  • crime_major_head_id  → CrimeMajorHead enum       (DEFERRED)
  • crime_minor_head_id  → CrimeMinorHead enum       (DEFERRED)
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CaseMaster(BaseModel):
    """
    Central domain entity representing a single FIR / Case
    registered in the Police FIR System.

    Maps directly to the CaseMaster table in the ER diagram.
    All field names follow Python snake_case conventions.
    """

    model_config = ConfigDict(from_attributes=True)

    # ----------------------------------------------------------
    # Primary Identifier
    # ----------------------------------------------------------

    # Unique system-generated identifier for the case record.
    # Serves as the primary key in the datastore.
    case_master_id: Optional[str] = None

    # ----------------------------------------------------------
    # FIR Registration Identifiers
    # ----------------------------------------------------------

    # Official Crime Number assigned by the police station.
    # Format is station-specific (e.g., "0045/2026").
    crime_no: str

    # Court-assigned Case Number after chargesheet is filed.
    # Nullable because it is assigned post-investigation.
    case_no: Optional[str] = None

    # ----------------------------------------------------------
    # Temporal Fields — Registration
    # ----------------------------------------------------------

    # Date and time the FIR was officially registered.
    crime_registered_date: datetime

    # ----------------------------------------------------------
    # Reference IDs — Police Personnel
    # ----------------------------------------------------------

    # ID of the investigating officer assigned to this case.
    # References: PolicePerson module (NOT YET IMPLEMENTED).
    # Will become a typed foreign key in a future phase.
    police_person_id: Optional[int] = None

    # ID of the police station where the FIR was registered.
    # References: PoliceStation module (NOT YET IMPLEMENTED).
    # Will become a typed foreign key in a future phase.
    police_station_id: int

    # ----------------------------------------------------------
    # Reference IDs — Classification & Categorization
    # ----------------------------------------------------------

    # ID of the case category (e.g., Cognizable, Non-Cognizable).
    # References: CaseCategory lookup (NOT YET IMPLEMENTED).
    # ENUM CANDIDATE — finite, stable set of values.
    case_category_id: Optional[int] = None

    # ID indicating the gravity/severity of the offence.
    # References: GravityOffence lookup (NOT YET IMPLEMENTED).
    # ENUM CANDIDATE — conditionally; depends on jurisdiction count.
    gravity_offence_id: Optional[int] = None

    # Major classification head of the crime (e.g., "Crimes Against Person").
    # References: CrimeMajorHead lookup (NOT YET IMPLEMENTED).
    # Deferred from Enum — potentially large and jurisdiction-specific.
    crime_major_head_id: Optional[int] = None

    # Sub-classification under the major head (e.g., "Murder", "Assault").
    # References: CrimeMinorHead lookup (NOT YET IMPLEMENTED).
    # Deferred from Enum — many-to-one with major head; too granular.
    crime_minor_head_id: Optional[int] = None

    # ----------------------------------------------------------
    # Reference IDs — Case Lifecycle
    # ----------------------------------------------------------

    # Current status of the case in its lifecycle.
    # References: CaseStatus lookup (NOT YET IMPLEMENTED).
    # ENUM CANDIDATE — finite set: Registered, Under Investigation,
    # Chargesheeted, Closed, Transferred, etc.
    case_status_id: Optional[int] = None

    # ID of the court where the case is being tried.
    # References: Court module (NOT YET IMPLEMENTED).
    # Will become a typed foreign key in a future phase.
    # Nullable because court is assigned after chargesheet filing.
    court_id: Optional[int] = None

    # ----------------------------------------------------------
    # Temporal Fields — Incident Window
    # ----------------------------------------------------------

    # Start date/time of the incident.
    # Used to define the temporal window of the crime.
    incident_from_date: Optional[datetime] = None

    # End date/time of the incident.
    # Together with incident_from_date, defines the incident duration.
    incident_to_date: Optional[datetime] = None

    # Date and time the information was received at the police station.
    # May differ from crime_registered_date (e.g., delayed reporting).
    info_received_ps_date: Optional[datetime] = None

    # ----------------------------------------------------------
    # Geospatial Fields
    # ----------------------------------------------------------

    # GPS latitude of the incident location.
    # Used for geospatial analytics and heatmap generation.
    # Will feed into the Neo4j Knowledge Graph for spatial queries.
    latitude: Optional[float] = None

    # GPS longitude of the incident location.
    # Used for geospatial analytics and heatmap generation.
    # Will feed into the Neo4j Knowledge Graph for spatial queries.
    longitude: Optional[float] = None

    # ----------------------------------------------------------
    # Narrative / Descriptive Content
    # ----------------------------------------------------------

    # Free-text summary of the incident as recorded in the FIR.
    # Primary input for the AI NLP analysis pipeline.
    # Will be processed for: entity extraction, sentiment analysis,
    # crime pattern matching, and knowledge graph population.
    brief_facts: Optional[str] = None

    # ----------------------------------------------------------
    # Audit Fields
    # ----------------------------------------------------------

    # Timestamp when this record was first created.
    # Auto-populated by the repository layer.
    created_at: Optional[datetime] = None

    # Timestamp of the most recent update to this record.
    # Auto-populated by the repository layer on each mutation.
    updated_at: Optional[datetime] = None
